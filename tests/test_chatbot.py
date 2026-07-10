from src.chatbot import ask

def test_chatbot():
    answer = ask("What is diabetes?")
    print(answer)
    assert answer is not None