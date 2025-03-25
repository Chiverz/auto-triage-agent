import streamlit as st
import asyncio
from chatbot import chat_with_agent  # Import chat function

# Streamlit UI
st.title("Chat with AI 🤖")
st.write("Ask anything, and the assistant will respond!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []  # Ensures messages persist

# Display chat history
for message in st.session_state.messages:
    role = "👤 You: " if message["role"] == "user" else "🤖 Assistant: "
    st.markdown(f"**{role}** {message['content']}")

# User input box
user_input = st.text_input("Type your message:", key="user_input")

# Process input when the user submits a message
if st.button("Send") and user_input:
    # Append user message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Send full conversation history to AI assistant
    response = asyncio.run(chat_with_agent(st.session_state.messages))

    # Append AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response.final_output})

    # Clear input field
    st.experimental_set_query_params()  # Workaround to clear input field
    st.rerun()  # Refresh UI to show new messages
