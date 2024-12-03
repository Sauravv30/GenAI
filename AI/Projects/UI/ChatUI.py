import subprocess
import sys

import streamlit as st
import requests

UPLOAD_URL = "http://localhost:8000/upload"
QUESTION_URL = "http://localhost:8000/ask"
WEB_URL = "http://localhost:8000/url"


def uploadFile(file):
    files = {"file": (file.name, file)}
    resp = requests.post(url=UPLOAD_URL, files=files)
    output = resp.json().get('response')
    if resp.status_code == 200:
        pass
        # side.success(output)
    else:
        side.error("Upload error")


def upload_web_content(url: str):
    resp = requests.post(url=WEB_URL, json={"url": web_url},
                         headers={'accept': 'application/json', "Content-Type": 'application/json'})
    output = resp.json().get('response')
    if resp.status_code == 200:
        pass
        # side.success(output)
    else:
        side.error("Content upload error")


st.title(":blue[Chat]bot :sunglasses:")
side = st.sidebar
side.title("Settings")
session_name = side.text_input("Username", value="Default")
source = side.selectbox('Choose Data Source', ['Nothing', 'PDF', 'WebUrl', 'Text', 'Database'])
source_path = ""
submit_button = st.empty()

if source == "Nothing":
    pass

elif source == "PDF" or source == "Text":
    uploaded_file = side.file_uploader("Upload PDF", type=["pdf", "txt"], accept_multiple_files=False)
    side.button("Submit", on_click=uploadFile, args=(uploaded_file,), use_container_width=True)


elif source == "WebUrl":
    web_url = side.text_input("WebUrl")
    side.button("Submit", on_click=upload_web_content, args=(web_url,))

elif source == "Database":
    pass

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
        response = requests.post(url=QUESTION_URL, json={
            "question": prompt,
            "sessionId": session_name
        }, headers={'accept': 'application/json', "Content-Type": 'application/json'})
        output = response.json()
        if response.status_code == 200:
            st.session_state.messages.append(
                {"role": "assistant", "content": output})
            st.chat_message("assistant").write(output)
        else:
            st.error(f"{response.text}")

if __name__ == "main":
    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        subprocess.run(["streamlit", "run", sys.argv[0]])
    else:
        print("Use python command streamlit run ChatUI.py")
