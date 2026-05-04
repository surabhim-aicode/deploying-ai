import sys

from dotenv import load_dotenv
from gradio import context
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
import os

DB_DIR = "chroma_db"
sys.path.append('../../05_src/')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, "../../.secrets")
load_dotenv('../../../05_src/.secrets')
API_GATEWAY_KEY = os.getenv("API_GATEWAY_KEY")
load_dotenv(dotenv_path)
#print(os.getenv("API_GATEWAY_KEY")) 
load_dotenv(dotenv_path)

class SemanticService:
    def __init__(self):
        self.embedding = OpenAIEmbeddings(
    model="text-embedding-3-small",
    openai_api_key="any-value", 
    openai_api_base="https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1",
    default_headers={
        "x-api-key": os.getenv("API_GATEWAY_KEY")
    }
)

        #print("🔄 Rebuilding ChromaDB...")
        self._create_db()

        self.db = Chroma(persist_directory=DB_DIR, embedding_function=self.embedding)
    
    PROJECT_ROOT = os.path.abspath(
    os.path.join(BASE_DIR, "..", "..", "..")
)

    pdf_path = os.path.join(
    PROJECT_ROOT,
    "02_activities",
    "documents",
    "ai_report_2025.pdf"
 )

    def _create_db(self):
       # print("📥 Loading PDF...")
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        # print("📄 PDF PATH:", self.pdf_path)
        # print("📄 EXISTS:", os.path.exists(self.pdf_path))
        # print(f"✅ Loaded {len(documents)} pages")
        splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=100)
        docs = splitter.split_documents(documents)
        # print(f"✂️ Split into {len(docs)} chunks")
        db = Chroma.from_documents(docs, self.embedding, persist_directory=DB_DIR)
        db.persist()
        print("💾 ChromaDB created successfully!")

    def query(self, question):

     results = self.db.similarity_search_with_score(question, k=4)

     results = sorted(results, key=lambda x: x[1])

     best_doc,best_score = results[0]

     cutoff = best_score + 0.15

     filtered = [doc for doc, score in results if score <= cutoff]
     print(f"🔍 Found {len(filtered)} relevant chunks (score <= {cutoff:.2f})")
     print(f"Best score: {best_score:.4f}")
     # safety check: still ensure relevance
     if best_score > 0.95:
        return "❌ No relevant information found in the document."
     return best_doc.page_content