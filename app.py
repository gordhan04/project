# Streamlit frontend will be here
import streamlit as st
import os
import tempfile
from rag_engine import process_document_to_chroma, get_rag_chain
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Annual Report Analyst", layout="wide")
st.title("📊 Annual Report Analyst (India/US)")

# Sidebar for Setup
with st.sidebar:
    st.header("Upload Report")
    uploaded_file = st.file_uploader("Upload PDF (10-K or Annual Report)", type=["pdf"])
    
    if uploaded_file and "vectorstore" not in st.session_state:
        with st.spinner("Processing with Docling (Parsing Tables...)..."):
            # Save temp file for Docling to read
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            # Process
            st.session_state.vectorstore = process_document_to_chroma(tmp_path)
            st.success("Report Indexed Successfully!")
            os.remove(tmp_path) # Cleanup

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about Revenue, Risks, or Strategy..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    if "vectorstore" in st.session_state:
        chain = get_rag_chain(st.session_state.vectorstore)
        with st.spinner("Analyzing..."):
            response = chain.invoke({"input": prompt})
            answer = response["answer"]
            
            # Append Sources (Portfolio "Wow" Factor)
            sources = list(set([doc.metadata.get('source', 'Unknown') for doc in response['context']]))
            # Note: Docling metadata might need inspection to get exact page numbers perfectly, 
            # but this is a good start.
            
    else:
        answer = "Please upload a document first to start the analysis."

    # Display assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)