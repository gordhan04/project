# 📊 Annual Report Analyst (RAG-based Financial Document AI)

An AI-powered **Annual Report Analyst** that allows users to upload company annual reports / 10-K PDFs and ask intelligent questions about **financials, risks, strategy, and KPIs** using a **Retrieval-Augmented Generation (RAG)** pipeline.

This project is designed as a **portfolio-grade, production-style application**, not a demo script.

---

## 🚀 Key Features

### 1️⃣ Conversational Financial Q&A (RAG)

* Ask natural language questions about annual reports
* Answers are grounded strictly in document context
* Uses **history-aware retrieval** to understand follow-up questions

Example:

> "What is the revenue?"
> "How did it change compared to last year?"

The system automatically reformulates the second question using chat history.

---

### 2️⃣ KPI Mode (Business-Focused Analysis)

Predefined analytical modes for quick insights:

* 📈 **Revenue & Profitability**
  Growth trends, margins, YoY comparisons

* ⚠️ **Risk Factors**
  Regulatory risks, operational risks, red flags

* 💰 **Cash Flow Health**
  Operating cash flow, debt signals, liquidity

This makes the app useful not only for Q&A, but also for **executive-level analysis**.

---

### 3️⃣ Citation Confidence & Source Transparency

Every answer includes:

* Source document chunks
* Page numbers
* A **confidence indicator**:

| Confidence | Meaning                           |
| ---------- | --------------------------------- |
| High       | Multiple consistent sources found |
| Medium     | Limited but relevant context      |
| Low        | Weak or partial evidence          |

This improves trust and reduces hallucination.

---

### 4️⃣ Streaming Responses (Real-time UX)

* Responses stream token-by-token
* Feels fast and interactive
* Suitable for long analytical answers

---

### 5️⃣ Robust Session & Reset Handling

* Logical DB wipe (vector store reset)
* Optional physical cleanup
* Clean session state reset

Designed to avoid stale embeddings or corrupted sessions.

---

## 🧠 Architecture Overview

```
User (Streamlit UI)
   │
   ▼
History-aware Retriever
   │   (Rewrites query using chat memory)
   ▼
Vector Store (Chroma + BGE Embeddings)
   │
   ▼
LLM (Groq – low latency)
   │
   ▼
Grounded Answer + Sources
```

---

## 🧩 Tech Stack

| Component     | Technology                |
| ------------- | ------------------------- |
| Frontend      | Streamlit                 |
| LLM           | Groq (openai/gpt-oss-20b) |
| Embeddings    | BAAI/bge-small-en-v1.5    |
| Vector DB     | Chroma                    |
| PDF Loader    | PyMuPDF                   |
| RAG Framework | LangChain                 |

---

## 🔍 Why These Choices?

### 🔹 History-Aware Retriever

* Solves vague follow-up questions
* Mimics how analysts ask sequential questions

### 🔹 BGE Embeddings

* Strong performance on financial & factual text
* Lightweight and fast

### 🔹 Groq LLM

* Extremely low latency
* Ideal for streaming UX

---

## 🛠️ How to Run Locally

```bash
git clone https://github.com/gordhan04/project.git
cd project

pip install -r requirements.txt

# Add your API key
cp .env.example .env

streamlit run app.py
```

---

## � Example Questions

* What is the revenue growth over the last 3 years?
* What are the major risk factors mentioned?
* Are there any red flags in cash flow?
* Summarize management strategy

---

## 🎯 Portfolio Value

This project demonstrates:

* Real-world RAG architecture
* Document-grounded reasoning
* Business-focused AI usage
* Production-style Streamlit application

It is suitable for:

* Data Science portfolios
* AI Engineer roles
* Agentic AI / RAG-based system interviews

---

## � Future Improvements

* Multi-document comparison
* Table-aware financial parsing
* KPI dashboards
* Exportable analysis reports
📊 Analyze Indian Annual & Integrated Reports

📈 Extract financial performance (Standalone & Consolidated)

⚠️ Identify regulatory and compliance risks (SEBI / MCA)

💰 Evaluate cash flow, debt, and dividend policies

🧾 Understand Related Party Transactions

📄 Source-backed answers with page-level citations

🔍 Confidence scoring for analytical reliability
---

## � Author

**Govardhan Rajpurohit**
Aspiring AI / Data Science Engineer
Focused on RAG systems, Agentic AI, and applied ML
