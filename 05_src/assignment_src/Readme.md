# 🧠 Surabhi AI Assistant – Multi-Service Conversational System

## 📌 Overview

This project is a conversational AI assistant built using a **multi-service architecture**.  
It integrates:

- 🌐 API-based service  
- 🔍 Semantic Search (RAG using ChromaDB)  
- 🧩 MCP Tool-based Web Search (Glama MCP Server)  
- 💬 Chat UI (Gradio) with memory (LangGraph)  

The assistant can:
- Answer general queries  
- Retrieve information from documents  
- Perform real-time web search  
- Maintain conversational context  

---

# 🏗️ Architecture

User → Gradio Chat UI → Memory (LangGraph)
↓
Intent Routing
↓
| API Service | Semantic | MCP Tool |

↓
Response → Chat UI


---

# 🧩 SERVICES

---

## 🔹 Service 1: API Service

### 📌 Purpose
Fetch real-world data from an external API and convert it into a user-friendly response.

### ⚙️ Functionality
- Calls external APIs (e.g., weather)
- Transforms raw data into readable natural language

### 💡 Example
User: *"What is the weather in Toronto?"*  
→ API called → formatted response returned  

---

## 🔹 Service 2: Semantic Search (RAG with ChromaDB)

### 📌 Purpose
Answer questions using **custom or internal  PDF documents** via semantic similarity search.

---

## 📚 Data Source
- PDF file: `ai_report_2025.pdf`

---

## 🧠 How It Works

#### 1. Document Loading

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(pdf_path)
documents = loader.load()
```
#### 2. Chunking (Text Splitting)

Large documents are split into smaller chunks:
```python
from langchain_text_splitters import CharacterTextSplitter
splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=100)
docs = splitter.split_documents(documents)
```
📌 Why chunking?
Improves retrieval accuracy
Keeps context manageable
Enables semantic matching

#### 3. Embedding Generation

- Each chunk is converted into a vector using OpenAI embeddings:
```python
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
```
-📌 What is embedding?

Text → numerical vector

Example:

"AI is powerful" → [0.21, -0.44, ...]

#### 4. Storage in ChromaDB
```python
from langchain_community.vectorstores import Chroma

db = Chroma.from_documents(docs, embeddings, persist_directory="chroma_db")
db.persist()
```
#### 5. Query Processing

When a user asks a question:

Query → converted to embedding
Similar chunks retrieved
Relevant content returned
🔍 Top-K Retrieval (k=2)
```python
results = db.similarity_search(query, k=4)
```
📌 What is K=4?
Retrieves top 4 most relevant chunks
Improves precision and relevance
Keeps responses concise
💡 Example

User: "Explain AI trends in 2025"

→ Top 4 relevant chunks retrieved
→ Response generated from document

🎯 Benefits

✔ Reduces hallucination
✔ Uses real document knowledge
✔ Context-aware answers

## 🔹Service 3: MCP Tool Service (Web Search via Glama)
📌 Purpose

Enable the assistant to perform real-time web search using an MCP server.

🔧 MCP Server Used

We use the following MCP server from Glama:

https://glama.ai/mcp/servers/ConechoAI/openai-websearch-mcp
⚙️ Implementation

The tool is configured as:
```python
{
  "type": "mcp",
  "server_label": "openai-websearch-mcp",
  "server_url": "https://glama.ai/mcp/servers/ConechoAI/openai-websearch-mcp"
}
```
🧠 How It Works
User asks a query (e.g., latest news)
Model decides to use MCP tool
Request sent to web search MCP server
Server retrieves real-time web data
Model generates final response using that data
💡 Example

User: "What are the latest AI developments?"

→ MCP tool performs web search
→ Returns updated and relevant information

🎯 Benefits

✔ Real-time information
✔ Access to external knowledge
✔ Improves answer freshness and accuracy

## 🧠 MEMORY (LangGraph)
📌 Purpose

Maintain short-term conversation context

⚙️ Implementation
```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
```
💡 Example

User: "My name is Surabhi"
Later: "What is my name?"

→ System remembers: Surabhi

## 💬 CHAT UI (Gradio)
📌 Implementation

The UI is built using Gradio Chatbot component.

Features
Chat-based interface
Role-based messages (user, assistant)
Interactive message input
Maintains chat history during session
Example UI Flow
User types message
Message passed to backend (chat() function)
Service routing decides which service to use
Response displayed in chat

## 🚧 GUARDRAILS

The system prevents:

- ❌ Restricted topics:
- Cats / Dogs
- Horoscope / Zodiac
- Taylor Swift
- ❌ System prompt exposure

## 📦 TECH STACK
- Python
- OpenAI API (via API Gateway)
- LangChain
- LangGraph (memory)
- ChromaDB (vector database)
- Gradio (chat UI)
- MCP (Glama web search server)

## 🚀 KEY DESIGN DECISIONS
- Modular service-based architecture
- RAG for document-based QA
- ChromaDB for lightweight vector storage
- MCP for real-time tool usage
- LangGraph for memory management
 
## 🏁 SUMMARY

This project demonstrates:

- ✔ Multi-service conversational AI system
- ✔ Semantic search with embeddings
- ✔ PDF-based question answering