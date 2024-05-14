import streamlit as st
import time
import logging
from chat_generator import response_generator

logging.basicConfig(filename='chat.log', filemode='w+', level=logging.INFO)
_logger = logging.getLogger('chat_app')
_logger.setLevel(logging.INFO)

st.title("Streaming Chat Test")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    start = time.time()
    with st.chat_message("assistant"):
        response = st.write_stream(response_generator(st.session_state.messages))
    end = time.time()

    _logger.info(f"Total Time: {end-start}")
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})