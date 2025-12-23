# The logic (rag pipeline) Docling+chroma+groq
import os
from dotenv import load_dotenv  # <--- IMPORT THIS

# Load environment variables from .env file immediately
load_dotenv() 
# Now checking if the key is loaded (Optional debugging step)
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("GROQ_API_KEY not found. Please check your .env file.")

from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_groq import ChatGroq
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate

# 1. Load and Process Document with Docling
def process_document_to_chroma(uploaded_file_path):
    # Docling is powerful: It converts PDF tables to Markdown tables automatically
    
    loader = PDFPlumberLoader(uploaded_file_path)

    
    docs = loader.load()
    
    # 2. Smart Splitting for Reports
    # First, split by Headers (H1, H2, H3) to keep sections like "Financial Results" together
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    md_header_splits = markdown_splitter.split_text(docs[0].page_content)

    # Then chunk recursively to fit context windows
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1200, 
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(md_header_splits)
    
    # 3. Embeddings & Vector DB
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # Persist to local disk so we don't re-process every time
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=embeddings,
        persist_directory="./chroma_db"
    )
    return vectorstore

# 4. Create the Chat Chain
def get_rag_chain(vectorstore):
    llm = ChatGroq(
        model="llama-3.1-8b-instant",  # Strong reasoning model for finance
        temperature=0
    )
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5} # Fetch top 5 relevant chunks
    )

    system_prompt = (
        "You are an expert Financial Analyst reading an Annual Report. "
        "Use the following pieces of retrieved context to answer the question. "
        "If the context contains a Markdown table, analyze the rows and columns carefully. "
        "If you don't know the answer, say that you don't know. "
        "\n\n"
        "{context}"
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain