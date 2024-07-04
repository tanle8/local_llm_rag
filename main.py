import os
import tempfile
import streamlit as st
from streamlit_chat import message
from rag import ChatPDF
import PyPDF2

# For debug
import traceback

# Page configuration and State management
# Streamlit uses st.session_state to maintain the state across interactions.
# This state includes messages, uploaded files, and the instance of the ChatPDF
# class.
st.set_page_config(page_title="Chat PDF")


def display_messages():
    """Display the conversation history."""
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()



def validate_input(input_text: str):
    if not input_text:
        return False, "Please enter a message."
    if len(input_text) < 3:
        return False, "Input is too short."
    return True, ""

def process_input():
    """Handles new user input, queries the ChatPDF instance, and appends
    responses to the session state.
    """
    if st.session_state["user_input"] and\
       len(st.session_state["user_input"].strip()) > 0:

        user_text = st.session_state["user_input"].strip()
        is_valid, validation_message = validate_input(user_text)
        if not is_valid:
            st.session_state["messages"].append((validation_message, False))
            return

        # Continue with existing logic if the input is valid
        try:
            with st.session_state["thinking_spinner"], st.spinner("Thinking..."):
                agent_text = st.session_state["assistant"].ask(user_text)
        except Exception as e:
            agent_text = "An error occurred while processing your request."
            st.error(f"Error during processing: {e}")
            traceback.print_exc()   # for console-based debugging

        st.session_state["messages"].append((user_text, True))
        st.session_state["messages"].append((agent_text, False))

def validate_pdf_content(file_path: str):
    try:
        # Implement a simple check to see if the PDF can be opened and read.
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            if len(reader.pages) == 0:
                return False, "The PDF contains no readable pages."
    except PyPDF2.errors.PdfReadError as e:
        return False, f"PDF could not be read: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"

    return True, ""


def read_and_save_file():
    try:
        st.session_state["assistant"].clear()
        st.session_state["messages"] = []
        st.session_state["user_input"] = ""

        for file in st.session_state["file_uploader"]:
            try:
                with tempfile.NamedTemporaryFile(delete=False) as tf:
                    tf.write(file.getbuffer())
                    file_path = tf.name

                is_valid, validation_message = validate_pdf_content(file_path)
                if not is_valid:
                    st.error(validation_message)
                    os.remove(file_path)
                    continue

                with st.session_state["ingestion_spinner"], \
                     st.spinner(f"Ingesting {file.name}"):
                    st.session_state["assistant"].ingest(file_path)
            finally:
                os.remove(file_path)
    except Exception as e:
        st.error(f"Failed to process the file: {e}")
        traceback.print_exc()  # for detailed debug information in the console


def page():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["assistant"] = ChatPDF()

    st.header("Chat with your PDF 💬📚")

    # Allow the user to upload PDF files. When a file is uploaded,
    # read_and_save_file function is triggered. This function saves the
    # uploaded file temporarily, then passes it io ChatPDF.ingest()
    # for processing. and finally deletes the temporary file.
    st.subheader("Upload a document")
    st.file_uploader(
        "Upload document",
        type=["pdf"],
        key="file_uploader",
        on_change=read_and_save_file,
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.session_state["ingestion_spinner"] = st.empty()

    display_messages()
    st.text_input("Message", key="user_input", on_change=process_input)


if __name__ == "__main__":
    page()
