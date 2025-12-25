import streamlit as st

def apply_custom_styles():
    """Injects all CSS styles for the app."""
    st.markdown("""
    <style>
    /* App background */
    .stApp { background-color: #0e1117; color: #eaeaea; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #161b22; }
    
    /* Chat bubbles */
    div[data-testid="stChatMessage"] {
        background-color: #161b22;
        border-radius: 12px;
        padding: 12px;
        margin-bottom: 10px;
    }
    
    /* User message specific color */
    div[data-testid="stChatMessage"]:has(span:contains("user")) {
        background-color: #1f6feb;
    }
    
    /* Input box */
    textarea { border-radius: 10px !important; }
    
    /* --- BUTTON STYLES --- */
    
    /* 1. Default/Secondary Buttons (Green) */
    button { 
        border-radius: 10px !important; 
        background-color: #238636 !important; 
        color: white !important; 
        border: none !important;
    }

    /* 2. Primary Buttons (The RESET Button) -> RED */
    /* This targets buttons with type="primary" specifically */
    button[kind="primary"] {
        background-color: #da3633 !important; /* Red Color */
        color: white !important;
        border: 1px solid #da3633 !important;
    }
    
    /* Hover effect for Red Button */
    button[kind="primary"]:hover {
        background-color: #b62324 !important; /* Darker Red on hover */
    }

    /* File uploader container */
    section[data-testid="stFileUploader"] {
        border: 2px dashed #30363d;
        border-radius: 12px;
        padding: 15px;
    }
    
    .block-container { padding-top: 2.8rem !important; }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Renders the gradient header and 'Try asking' section."""
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #1f6feb, #238636);
        padding: 20px;
        border-radius: 16px;
        color: white;
        margin-bottom: 80px;">
        <h2 style="margin: 0;">📊 Annual Report Analyst</h2>
        <p style="margin-top: 8px;">AI-powered RAG system for financial document analyzing</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 💡 Try asking:")
    st.markdown("""
    - What is the standalone vs consolidated revenue?
    - What are the key regulatory risks under SEBI / MCA?
    - Summarize related party transactions
    - Any red flags mentioned by auditors?
    - What dividend has been declared and why?
    """)

def render_sidebar_capabilities():
    """Renders the static capabilities text in sidebar."""
    st.markdown("---")
    st.markdown("### ⚙️ Capabilities")
    st.markdown("""
    - Revenue Analysis  
    - Risk Factors  
    - Management Discussion  
    - Strategy Insights  
    """)