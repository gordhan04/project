"""RAG Engine for financial document analysis using LangChain and Chroma."""

import os
from typing import List, Tuple
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_classic.chains.history_aware_retriever import create_history_aware_retriever

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

def process_document_to_chroma(uploaded_file_path: str):
    """Load PDF, chunk intelligently, create Chroma vector store.
    
    Args:
        uploaded_file_path: Path to the PDF file to process.
        
    Returns:
        Chroma vector store containing embedded documents.
    """

    def classify_section(text: str) -> str:
        """Classify document section to optimize chunking parameters.
        
        Args:
            text: Content to classify.
            
        Returns:
            Section category for appropriate chunk sizing.
        """
        t = text.lower()
        if "management discussion" in t or "md&a" in t:
            return "mdna"
        if "risk" in t:
            return "risk"
        if "financial statement" in t or "balance sheet" in t:
            return "financials"
        if "notes to" in t:
            return "notes"
        if "notice" in t or "e-voting" in t or "agm" in t:
            return "legal"
        return "other"

    # Load PDF documents
    loader = PyMuPDFLoader(uploaded_file_path)
    try:
        docs = loader.load()
    except Exception as e:
        raise RuntimeError(f"Failed to parse PDF: {str(e)}")
    
    # Filter and classify sections
    filtered_docs = []
    for doc in docs:
        section = classify_section(doc.page_content)
        # Skip legal/notice pages - they add noise without analytical value
        if section != "legal":
            doc.metadata["section"] = section
            filtered_docs.append(doc)
    def get_chunk_params(section: str) -> Tuple[int, int]:
        """Get optimal chunk size and overlap for document section.
        
        Financial content requires larger chunks to preserve context.
        """
        if section in ["financials", "notes"]:
            return 1800, 300  # Larger chunks for tables and numbers
        return 1200, 150  # Standard chunks for narrative text

    # Intelligently split documents based on section type
    all_splits = []
    for doc in filtered_docs:
        chunk_size, overlap = get_chunk_params(doc.metadata["section"])
        splitter = RecursiveCharacterTextSplitter(
           chunk_size=chunk_size,
            chunk_overlap=overlap
        )
        all_splits.extend(splitter.split_documents([doc]))
    
    # Create embeddings using BGE model (optimized for financial text)
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")
    
    # Create in-memory Chroma vector store with embedded documents
    vectorstore = Chroma.from_documents(
        documents=all_splits,
        embedding=embeddings
    )
    return vectorstore

def format_docs(docs: List) -> str:
    """Format retrieved documents for LLM context.
    
    Args:
        docs: List of retrieved document chunks.
        
    Returns:
        Formatted string with page numbers and content.
    """
    return "\n\n---\n\n".join(
        f"[Page {doc.metadata.get('page', '?')}]\n{doc.page_content}"
        for doc in docs
    )

def get_rag_chain(vectorstore: Chroma):
    """Build history-aware RAG chain for answering financial questions.
    
    Args:
        vectorstore: Chroma vector store with embedded documents.
        
    Returns:
        Tuple of (history_aware_retriever, generation_chain).
    """
    # Initialize LLM with streaming for real-time responses
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0,  # Deterministic answers for financial analysis
        streaming=True
    )
    
    # MMR retriever balances relevance and diversity
    retriever = vectorstore.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 6,  # Return top 6 relevant chunks
            "fetch_k": 20,  # Fetch more candidates for diversity
            "lambda_mult": 0.7  # 70% relevance, 30% diversity
        }
    )

    # STEP 1: Reformat follow-up questions using chat history
    # Example: "How did it change?" -> "How did the revenue change compared to last year?"
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question which might reference context in the chat history, "
        "formulate a standalone question which can be understood without the chat history. "
        "Do NOT answer the question, just reformulate it if needed and otherwise return it as is."
    )
    
    contextualize_q_prompt = ChatPromptTemplate.from_messages([
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])
    
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # STEP 2: Generate grounded answers from retrieved context
    system_prompt = (
        "You are an expert Financial Analyst specializing in annual report analysis. "
        "Use the retrieved context to answer questions about financial performance, risks, and strategy. "
        "When analyzing tables, carefully examine rows and columns. "
        "Expand financial terminology: 'revenue' includes 'total income', 'net sales', 'turnover'. "
        "If the answer is not in the context, say 'I don't have this information in the document.' "
        "Always be precise and cite specific figures when available.\n\n"
        "Context:\n{context}"
    )

    qa_prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ])

    # Compose the generation chain
    generation_chain = qa_prompt | llm | StrOutputParser()
    
    return history_aware_retriever, generation_chain