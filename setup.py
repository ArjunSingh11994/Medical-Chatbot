from setuptools import setup, find_packages


setup(
    name="llm_medical_chatbot",
    version="1.0.0",
    author="Arjun Singh",
    description="Medical chatbot",
    packages=find_packages(),
    install_requires=[
        "langchain",
        "faiss-cpu",
        "streamlit"
    ],
    python_requires=">=3.10",
)