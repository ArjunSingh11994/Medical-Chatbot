from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from src.config import (
    GROQ_API_KEY,
    LLM_MODEL,
    TEMPERATURE,
    MAX_TOKENS,
    SYSTEM_PROMPT
)

from src.retrieval import retrieve_documents


class MedicalChatbot:

    def __init__(self):

        print("="*60)
        print("Loading LLM...")
        print("="*60)

        self.llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name=LLM_MODEL,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS
        )

        self.prompt = ChatPromptTemplate.from_messages([
            ("system",SYSTEM_PROMPT),
            ("human", """
             Context
             {context}
             Question
             {question}
             Answer:
             """)])

        self.chain = (
            self.prompt
            |
            self.llm
            |
            StrOutputParser())


    def format_context(self, docs):

        context = "\n\n".join(
            [doc.page_content
             for doc in docs])

        return context

  

    def ask(self, question):

        docs = retrieve_documents(question)

        context = self.format_context(docs)

        answer = self.chain.invoke(

            {"context": context,
             "question": question
             })

        return {
            "question": question,
            "answer": answer,
            "documents": docs}


chatbot = MedicalChatbot()


def ask(question):

    return chatbot.ask(question)