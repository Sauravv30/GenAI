import os

import streamlit as st

from config.configuration import Configuration
from loaders.loader import PDFLoader, WebLoader
from preprocessing.preprocessing import PreProcessing
from processing.processing import Processing
from service.userservice import UserService

# User request handling


### Side panel ###
st.title(":blue[Cool] Chatbot :sunglasses:")
side = st.sidebar
side.title("Settings")

st.session_state.session_name = side.text_input("Username", value="Default")
source = side.selectbox('Choose Data Source', ['PDF', 'WebUrl', 'Database'])
loader = None
source_path = ""
if source == "PDF":

    # Define the directory where you want to save the uploaded files
    url = "../uploaded_pdfs"

    # Create the directory if it doesn't exist
    if not os.path.exists(url):
        os.makedirs(url)
    try:
        uploaded_file = side.file_uploader("Upload PDF", type="pdf", accept_multiple_files=False)
        if uploaded_file:
            source_path = os.path.join(url, uploaded_file.name)
            with open(source_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            side.success("Done")
            loader = PDFLoader(path=source_path).load()
    except IndexError as e:
        side.warning("Please upload file")

if source == "WebUrl":
    source_path = side.text_input("Url:").strip()
    if source_path:
        side.success("Done")
        loader = WebLoader(path=source_path).load()

    else:
        side.warning("Please enter url")


if None is st.session_state.get("service") and loader:
    with st.spinner():
        print("Creating service................")
        Configuration(None).load()

        # documents = PDFLoader(path=f"../uploaded_pdfs/Resume.pdf").load()
        retriever = PreProcessing().do_preprocessing(loader)
        # Processing

        processing = Processing()
        chain = processing.create_tools_chain(retriever)
        service = UserService(processing, chain)
        st.session_state["service"] = service


def clear_previous_context():
    if "service" in st.session_state and st.session_state.service:
        st.session_state["service"] = None
        # print(f"Cleared context ")
        # load_service()


side.button("Clear", on_click=clear_previous_context)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi, How can i help you today ?"}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

prompt = st.chat_input(placeholder="What is Generative AI ?")
if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.spinner():
        history, response = st.session_state["service"].invoke_user_request(prompt, st.session_state.session_name)
        st.session_state.messages.append(
            {"role": "assistant", "content": response['output']})
        st.write(f"{response['output']}")
