import streamlit as st
from WebChatbotWithLLAMAStreamUI import ChatBot

bot = ChatBot()

def url_button_clicked():
    bot.submit_request(url)


def question_button_clicked():
    st.write(bot.submit_question(question))


st.title("Web Chatbot")

url = st.text_input("Enter any blog url",
                    value="https://medium.com/@gayani.parameswaran/advanced-q-a-chatbot-with-chain-and-retriever-using-langchain-7ad735b1d238")
button = st.button("Send", on_click=url_button_clicked)

question = st.text_input("Enter your question")
st.button("Submit", on_click=question_button_clicked)
