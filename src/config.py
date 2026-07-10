# Central configuration file for the Medical RAG Chatbot

from dotenv import load_dotenv
import os

# Load Environment Variables

load_dotenv()

# API Keys

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in .env")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")

# Project Paths


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
PDF_PATH = os.path.join(DATA_DIR, "Medical_book.pdf")

# Embedding Model
# ==========================================================

EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

# Cross Encoder Reranker
# ==========================================================

RERANKER_MODEL = "BAAI/bge-reranker-large"

# Pinecone Configuration
# ==========================================================

INDEX_NAME = "medical-chatbot"
VECTOR_DIMENSION = 384
METRIC = "mmr"
CLOUD = "aws"
REGION = "us-east-1"

# Chunking Configuration
# ==========================================================

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
SEPARATORS = [
    "\n\n",
    "\n",
    ". ",
    " ",
    ""
]
# Retriever Configuration
# ==========================================================

TOP_K = 5
SEARCH_TYPE = "similarity"
BM25_WEIGHT = 0.4
VECTOR_WEIGHT = 0.6

# Groq LLM Configuration
# ==========================================================

LLM_MODEL = "llama-3.3-70b-versatile"
TEMPERATURE = 0.2
MAX_TOKENS = 1024

# Prompt Configuration
# ==========================================================

SYSTEM_PROMPT = """
You are an expert AI Medical Assistant.

Answer ONLY from the retrieved medical context.

If the answer is not present in the context,
reply:

'I couldn't find this information in the medical book.'

Do not hallucinate.

Always answer in simple English.

If possible:
- Use bullet points
- Explain medical terms
- Keep the answer concise
"""

# Device
# ==========================================================

try:
    import torch

    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

except Exception:
    DEVICE = "cpu"

# Logging
# ==========================================================

LOG_LEVEL = "INFO"

# Display Configuration
# ==========================================================

PRINT_TOP_K_DOCUMENTS = True

PRINT_RERANK_SCORES = True

PRINT_RETRIEVED_CONTEXT = False