from sentence_transformers import CrossEncoder
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever
from src.preprocessing import (
    load_pdf,
    filter_documents,
    split_documents,
    get_vectorstore)
from src.config import (
    TOP_K,
    SEARCH_TYPE,
    VECTOR_WEIGHT,
    BM25_WEIGHT,
    RERANKER_MODEL)

class HybridRetriever:

    def __init__(self):
        print("=" * 60)
        print("Initializing Hybrid Retriever...")
        print("=" * 60)
        # Load Vector Store

        self.vectorstore = get_vectorstore()
        # Load Documents for BM25

        documents = load_pdf()
        documents = filter_documents(documents)
        chunks = split_documents(documents)
        # Vector Retriever
        
        self.vector_retriever = self.vectorstore.as_retriever(
            search_type=SEARCH_TYPE,
            search_kwargs={"k": TOP_K})
      
        # BM25 Retriever

        self.bm25_retriever = BM25Retriever.from_documents(chunks)

        self.bm25_retriever.k = TOP_K

        # Hybrid Retriever

        self.hybrid = EnsembleRetriever(retrievers=[
            self.bm25_retriever,
            self.vector_retriever],

            weights=[
                BM25_WEIGHT,
                VECTOR_WEIGHT])

        # Cross Encoder

        self.reranker = CrossEncoder(RERANKER_MODEL)
        print("Retriever Ready.")

    #######################################################

    def retrieve(self, query):
        """
        Retrieve documents using Hybrid Search
        """
        docs = self.hybrid.invoke(query)

        return docs

    #######################################################

    def rerank(self, query, docs):
        """
        Rerank retrieved documents.
        """
        pairs = [(query, doc.page_content)
            for doc in docs]
        scores = self.reranker.predict(pairs)
        ranked = sorted(zip(scores, docs),reverse=True,
            key=lambda x: x[0])
        final_docs = [
            doc
            for score, doc in ranked[:TOP_K]]

        return final_docs

    #######################################################

    def retrieve_and_rerank(self, query):
        """
        Complete Retrieval Pipeline
        """
        docs = self.retrieve(query)
        docs = self.rerank(query,docs)

        return docs

    #######################################################

    def show_documents(self, docs):
        """
        Print Retrieved Documents
        """
        print("=" * 80)
        print(f"Medical Book : {len(docs)}")
        print("=" * 80)

        for i, doc in enumerate(docs):
            print("\n")
            print("=" * 80)
            print(f"Rank : {i+1}")
            print("=" * 80)
            print("Metadata")
            print(doc.metadata)
            print()
            print(doc.page_content[:500])
            print()

##############################################################

retriever = HybridRetriever()

##############################################################

def retrieve(query):

    return retriever.retrieve(query)

##############################################################

def rerank(query, docs):

    return retriever.rerank(query, docs)

##############################################################

def retrieve_documents(query):

    return retriever.retrieve_and_rerank(query)