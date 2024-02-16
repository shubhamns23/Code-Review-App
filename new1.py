from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from io import StringIO
import streamlit as st
from dotenv import load_dotenv
import time
import base64
import re  # Importing regex module for pattern matching

# Load environment variables from a .env file into the application's environment
load_dotenv()

# Title and header for the Streamlit app
st.title("Let's do code review for your Python code")
st.header("Please upload your .py file here:")

# Function to download text content as a file using Streamlit
def text_downloader(raw_text):
    timestr = time.strftime("%Y%m%d-%H%M%S")  # Timestamp for filename
    b64 = base64.b64encode(raw_text.encode()).decode()  # Encode text in base64
    new_filename = "code_review_analysis_file_{}_.txt".format(timestr)  # New filename with timestamp
    st.markdown("#### Download File ✅###")
    href = f'<a href="data:file/txt;base64,{b64}" download="{new_filename}">Click Here!!</a>'  # HTML link for download
    st.markdown(href, unsafe_allow_html=True)

# Capture the .py file data
data = st.file_uploader("Upload python file", type=".py")

if data:
    # Create a StringIO object and initialize it with the decoded content of 'data'
    stringio = StringIO(data.getvalue().decode('utf-8'))

    # Read the content of the StringIO object and store it in the variable 'fetched_data'
    fetched_data = stringio.read()

    # Display the fetched code
    st.write(fetched_data)

    # Check for potentially harmful code
    if re.search(r'(?i)(eval|exec)', fetched_data):
        st.warning("Potentially harmful code detected! Avoid using 'eval' or 'exec' statements.")

    # Check for SQL injections
    if re.search(r'(?i)(select|insert|update|delete|union|drop|alter)', fetched_data):
        st.warning("Potential SQL injection detected! Avoid using raw SQL queries, use parameterized queries instead.")

    # Initialize a ChatOpenAI instance with the specified model name "gpt-3.5-turbo" and a temperature of 0.9
    chat = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.9)

    # Create a SystemMessage instance with information about the assistant's role
    systemMessage = SystemMessage(content="You are a code review assistant. Provide detailed suggestions to improve the given Python code by mentioning the existing code line by line with proper indentation.")

    # Create a HumanMessage instance with content read from the uploaded file
    humanMessage = HumanMessage(content=fetched_data)

    # Call the chat method of the ChatOpenAI instance, passing a list of messages containing the system and human messages
    finalResponse = chat([systemMessage, humanMessage])

    # Display review comments
    st.markdown(finalResponse.content)

    # Download the review comments as a file
    text_downloader(finalResponse.content)
