import os

import streamlit as st

from Service import CharService

st.title(":blue[Q&A Chatbot] :sunglasses: ")
container = st.container(border=False, height=550)


# st.title("Chatbot")
def reset_context():
    if "expensive_data" in st.session_state and st.session_state.expensive_data:
        print(f"Cleared context {st.session_state.clear()}")


## Side bar
side = st.sidebar
side.title("Settings")

st.session_state.session_name = side.text_input("Username", value="Default")
source = side.selectbox('Choose Data Source', ['PDF', 'WebUrl', 'Database'], on_change=reset_context)
# characters = {"human": ":hugging_face:", "ai": ":computer:"}
characters = {"human": "&#128512", "ai": "&#128373"}
characters_align = {"human": "right", "ai": "left"}
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
    except IndexError as e:
        side.warning("Please upload file")

if source == "WebUrl":
    source_path = side.text_input("Url:").strip()
    if source_path:
        side.success("Done")
    else:
        side.warning("Please enter url")


def load_chat(output):
    # if user_input:
    for message in output:
        container.markdown(f"""
        <div style="text-align: {characters_align[message.type]};">
            <p>{characters[message.type]} {message.content}</p>
        </div>
            """, unsafe_allow_html=True)


def reload():
    if "history" in st.session_state:
        load_chat(st.session_state.history)


# component_container = st.container()


# response_container = st.container(border=True)
# Function to add a message to the chat
def add_message():
    user_input = st.session_state.user_input
    bot_service = st.session_state.expensive_data
    if user_input:
        with st.spinner("Thinking..."):
            output, response = bot_service.invoke_user_request(question=user_input,
                                                               session_name=st.session_state.session_name)
            # load_chat(output)
            st.session_state.history = output
            # st.write(response['answer'])


user_question = st.text_input("Write your query here:", key='user_input')
submit_button = st.button("Send", type="primary", icon=":material/send:", on_click=add_message)

reload()


def load_bot(data_source, data_source_path):
    # Check that both source and source_path are provided
    service = CharService()
    if source and source_path:
        service.start_chat_bot(source=data_source, path=data_source_path)
        return service


# Initialize session state if it's the first time loading the bot
if "expensive_data" not in st.session_state:
    if source and source_path:
        with st.spinner("Initializing..."):
            st.session_state.expensive_data = load_bot(source, source_path)
            st.success("Ready to use")
    else:
        st.warning("Please initialize data source first")
