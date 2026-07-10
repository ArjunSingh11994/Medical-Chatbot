from src.retrieval import retrieve_documents


def test_retrieve_documents():

    docs = retrieve_documents("What is diabetes")

    assert docs is not None
    assert len(docs) > 0

    for i, doc in enumerate(docs):
        print("=" * 50)
        print(f"Rank {i+1}")
        print("Metadata : ",doc.metadata)
        print()
        print(doc.page_content[:500])