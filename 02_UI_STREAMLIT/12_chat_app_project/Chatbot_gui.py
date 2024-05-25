import streamlit as st
import random 
import time


st.title("Muzzamil's Bot")

# Initialization chat history
"""st.session_state.messages. For each message, it uses st.chat_message to create a chat bubble on the screen. The message["role"] determines the appearance of the chat bubble (whether it looks like it was sent by the user or the assistant). Then, st.markdown(message["content"]) displays the actual text of the message inside the chat bubble. It’s similar to scrolling through your chat history and seeing all the messages that have been exchanged."""
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

# Streamed response emulator
def response_generator():
    response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    for word in response.split():
        yield word + " "
        time.sleep(0.05)
# Display assistant response in chat message container
with st.chat_message("assistant"):
    response = st.write_stream(response_generator())
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": response})


"""This code snippet is for a chatbot application built with Streamlit, a Python library that simplifies the process of creating web apps. Here's a breakdown of what the code does with real-world examples:

1. **Streamlit Title**: `st.title("Muzzamil's Bot")` sets the title of the web page to "Muzzamil's Bot". It's like naming your shop to attract customers.

2. **Chat History Initialization**: The `if "messages" not in st.session_state:` block checks if there's an existing chat history. If not, it initializes an empty list. This is similar to opening a new notebook page for taking notes during a conversation.

3. **Displaying Messages**: The `for` loop iterates over the stored messages and displays them using `st.chat_message`. It's like reading previous messages on your phone's messaging app to catch up with the conversation.

4. **User Input**: `if prompt := st.chat_input("What is up?"):` captures the user's message when they type in the chat input box. It's akin to asking someone "What is up?" and waiting for their response.

5. **Display User Message**: The `with st.chat_message("user"):` block displays the user's message in the chat. It's like when you send a text, and it appears on your chat screen.

6. **Add User Message to History**: `st.session_state.messages.append({"role": "user", "content": prompt})` adds the user's message to the chat history. It's like saving a copy of the conversation in your diary.

7. **Streamed Response Emulator**: The `response_generator()` function simulates a typing effect for the chatbot's response, choosing randomly from a set of predefined messages. It's like someone typing a response to you in real-time.

8. **Display Assistant Response**: The `with st.chat_message("assistant"):` block shows the chatbot's response in the chat. It's the chatbot's turn to contribute to the conversation.

9. **Add Assistant Response to History**: Finally, the chatbot's response is added to the chat history, ensuring the conversation can be continued seamlessly.

In essence, this code creates a simple chatbot that can interact with users, store the conversation, and provide a dynamic response experience. It's like having a digital assistant ready to chat and help with inquiries."""