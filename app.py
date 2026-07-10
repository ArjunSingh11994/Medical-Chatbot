import streamlit as st
from src.chatbot import ask

st.set_page_config(page_title="Medical RAG Chatbot",
    page_icon="🩺",
    layout="wide")

st.title("🩺 Medical RAG Chatbot")

st.write("Ask any medical question. The chatbot answers using  medical book PDF knowledge base")

question = st.text_input("Enter your question:")

if st.button("Ask"):

    if question.strip() == "":
        st.warning("Please enter a question.")
    else:

        with st.spinner("Searching..."):
            result = ask(question)

        st.subheader("Answer")

        st.write(result["answer"])

        with st.expander("Retrieved Documents"):

            for i, doc in enumerate(result["documents"]):

                st.markdown(f"### Medical Book Answer {i+1}")

                st.write(doc.metadata)

                st.write(doc.page_content[:1000])

                st.divider()