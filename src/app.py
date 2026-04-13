"""Streamlit chat application with Gemini AI."""

import os

import streamlit as st
from dotenv import load_dotenv

from src.gemini_client import GeminiClient

# Load environment variables
load_dotenv()


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "client" not in st.session_state:
        st.session_state.client = None


def setup_page():
    """Configure the Streamlit page and title."""
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon="🤖",
        layout="centered",
    )
    st.title("🤖 Gemini Chatbot")
    st.caption("Powered by Google Gemini AI")


def get_api_key() -> str | None:
    """Retrieve API key from environment or user input."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        if api_key:
            st.session_state.client = GeminiClient(api_key=api_key)
    return api_key


def display_chat_history():
    """Render all previous messages from session state."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(prompt: str):
    """Process user input and generate AI response.

    Args:
        prompt: User's input message.
    """
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and display assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = st.session_state.client.send_message(prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Error: {str(e)}")


def main():
    """Main application entry point."""
    setup_page()
    initialize_session_state()

    api_key = get_api_key()
    if not api_key:
        st.warning("Please provide your Gemini API key to continue.")
        return

    # Initialize client if not already done
    if st.session_state.client is None:
        st.session_state.client = GeminiClient(api_key=api_key)

    # Start chat session with history
    if not hasattr(st.session_state, "chat_started") or not st.session_state.chat_started:
        # Convert message history to Gemini format
        history = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        st.session_state.client.start_chat(history=history)
        st.session_state.chat_started = True

    # Display chat history
    display_chat_history()

    # Handle user input
    if prompt := st.chat_input("Type your message..."):
        handle_user_input(prompt)


if __name__ == "__main__":
    main()
