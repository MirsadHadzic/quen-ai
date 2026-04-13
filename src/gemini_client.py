"""Gemini API client for handling chat conversations."""

import google.generativeai as genai
from google.generativeai.types import content_types


class GeminiClient:
    """Client for interacting with Google Gemini API."""

    def __init__(self, api_key: str, model_name: str = "gemini-flash-latest"):
        """Initialize the Gemini client.

        Args:
            api_key: Google Gemini API key.
            model_name: Name of the Gemini model to use.
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)
        self.chat = None

    def start_chat(self, history: list[dict] | None = None):
        """Start a new chat session.

        Args:
            history: Optional list of previous messages for context.
        """
        self.chat = self.model.start_chat(history=history or [])

    def send_message(self, message: str) -> str:
        """Send a message to the Gemini model and get the response.

        Args:
            message: User's input message.

        Returns:
            Model's response text.

        Raises:
            ValueError: If chat session hasn't been started.
        """
        if not self.chat:
            raise ValueError("Chat session not started. Call start_chat() first.")

        response = self.chat.send_message(message)
        return response.text

    def get_chat_history(self) -> list[dict]:
        """Get the current chat history.

        Returns:
            List of message dictionaries with 'role' and 'parts' keys.

        Raises:
            ValueError: If chat session hasn't been started.
        """
        if not self.chat:
            raise ValueError("Chat session not started. Call start_chat() first.")

        return self.chat.history
