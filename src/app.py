"""Streamlit chat aplikacija sa Gemini AI-om."""

import os

import streamlit as st
from dotenv import load_dotenv

from gemini_client import GeminiClient

# Učitaj varijable iz okruženja
load_dotenv()


def initialize_session_state():
    """Inicijalizuj Streamlit session state varijable."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "client" not in st.session_state:
        st.session_state.client = None


def setup_page():
    """Konfiguriraj Streamlit stranicu i naslov."""
    st.set_page_config(
        page_title="Gemini Chatbot",
        page_icon="🤖",
        layout="centered",
    )
    st.title("🤖 Gemini Chatbot")
    st.caption("Pokreće Google Gemini AI")


def get_api_key() -> str | None:
    """Preuzmi API ključ iz okruženja ili korisnikovog unosa."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        api_key = st.text_input("Unesite svoj Gemini API ključ:", type="password")
        if api_key:
            st.session_state.client = GeminiClient(api_key=api_key)
    return api_key


def display_chat_history():
    """Prikaži sve prethodne poruke iz session state-a."""
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def handle_user_input(prompt: str):
    """Obradi korisnikov unos i generiši AI odgovor.

    Args:
        prompt: Korisnikova ulazna poruka.
    """
    # Prikaži korisnikovu poruku
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generiši i prikaži odgovor asistenta
    with st.chat_message("assistant"):
        with st.spinner("Razmišljam..."):
            try:
                response = st.session_state.client.send_message(prompt)
                st.markdown(response)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )
            except Exception as e:
                st.error(f"Greška: {str(e)}")


def main():
    """Glavna ulazna tačka aplikacije."""
    setup_page()
    initialize_session_state()

    api_key = get_api_key()
    if not api_key:
        st.warning("Molimo unesite svoj Gemini API ključ za nastavak.")
        return

    # Inicijalizuj klijent ako već nije
    if st.session_state.client is None:
        st.session_state.client = GeminiClient(api_key=api_key)

    # Započni chat sesiju sa historijom
    if not hasattr(st.session_state, "chat_started") or not st.session_state.chat_started:
        # Pretvori historiju poruka u Gemini format
        history = []
        for msg in st.session_state.messages:
            role = "user" if msg["role"] == "user" else "model"
            history.append({"role": role, "parts": [msg["content"]]})

        st.session_state.client.start_chat(history=history)
        st.session_state.chat_started = True

    # Prikaži historiju chata
    display_chat_history()

    # Obradi korisnikov unos
    if prompt := st.chat_input("Napišite svoju poruku..."):
        handle_user_input(prompt)


if __name__ == "__main__":
    main()
