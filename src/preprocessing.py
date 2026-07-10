from typing import List
import os
import torch
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.config import (
    PDF_PATH,
    PINECONE_API_KEY,
    EMBEDDING_MODEL,
    INDEX_NAME,
    VECTOR_DIMENSION,
    METRIC,
    CLOUD,
    REGION,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SEPARATORS
)


# Load PDF
##############################################################

def load_pdf(pdf_path: str = PDF_PATH) -> List[Document]:
    """
    Load PDF using LangChain.
    """
    print("=" * 60)
    print("Loading PDF...")
    print("=" * 60)
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    print(f"Total Pages : {len(documents)}")
    return documents

# Filter Metadata
##############################################################

def filter_documents(documents: List[Document]) -> List[Document]:
    """   
    Keep only source metadata.
    """
    print("=" * 60)
    print("Filtering Metadata...")
    print("=" * 60)
    filtered_docs = []
    
    for doc in documents:
        filtered_docs.append(
            Document(page_content=doc.page_content,
                metadata={"source": doc.metadata.get("source", "")})
        )

    print(f"Filtered Pages : {len(filtered_docs)}")
    return filtered_docs

# Chunk Documents
##############################################################

def split_documents(documents: List[Document]) -> List[Document]:

    print("=" * 60)
    print("Creating Chunks...")
    print("=" * 60)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=SEPARATORS)

    chunks = splitter.split_documents(documents)
    print(f"Total Chunks : {len(chunks)}")
    return chunks

# Load Embedding Model
##############################################################

def load_embedding_model():

    print("=" * 60)
    print("Loading Embedding Model...")
    print("=" * 60)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL,
                                            model_kwargs={"device": device},
                                            encode_kwargs={"normalize_embeddings": True})

    print(f"Device : {device}")
    return embedding_model

# Connect Pinecone
##############################################################

def connect_pinecone():
    print("=" * 60)
    print("Connecting Pinecone...")
    print("=" * 60)

    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc

# Create Pinecone Index
##############################################################

def create_index(pc):
    print("=" * 60)
    print("Checking Pinecone Index...")
    print("=" * 60)

    if not pc.has_index(INDEX_NAME):
        print("Creating Index...")

        pc.create_index(name=INDEX_NAME,
            dimension=VECTOR_DIMENSION,
            metric=METRIC,
            spec=ServerlessSpec(
                cloud=CLOUD,
                region=REGION))

    else:
        print("Index Already Exists.")
    return pc.Index(INDEX_NAME)


# Upload Documents
##############################################################

def upload_documents(chunks, embedding_model):
    print("=" * 60)
    print("Uploading Chunks...")
    print("=" * 60)

    PineconeVectorStore.from_documents(documents=chunks,
        embedding=embedding_model,
        index_name=INDEX_NAME)

    print("Upload Completed.")


# Load Existing Vector Store
##############################################################

def load_vectorstore(embedding_model):

    print("=" * 60)
    print("Loading Existing Index...")
    print("=" * 60)

    vectorstore = PineconeVectorStore.from_existing_index(index_name=INDEX_NAME,
        embedding=embedding_model)

    return vectorstore


# Build Knowledge Base
##############################################################

def build_knowledge_base():
    """
    Run only one time.
    """
    documents = load_pdf()
    filtered_docs = filter_documents(documents)
    chunks = split_documents(filtered_docs)
    embedding_model = load_embedding_model()
    pc = connect_pinecone()
    create_index(pc)
    upload_documents(chunks,embedding_model)

    print("=" * 60)
    print("Knowledge Base Created Successfully")
    print("=" * 60)


# Get Existing Vector Store
##############################################################

def get_vectorstore():
    embedding_model = load_embedding_model()
    vectorstore = load_vectorstore(embedding_model)

    return vectorstore