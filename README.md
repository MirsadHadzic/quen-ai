# Gemini Chatbot

A Streamlit chatbot application powered by Google Gemini AI.

## Features

- 🌙 Dark theme UI
- 💬 Chat history with conversation memory
- 🔒 Secure API key loading from `.env`
- 🧩 Modular architecture (easy to swap AI models)

## Prerequisites

- Python 3.10+
- [uv](https://github.com/astral-sh/uv) package manager
- Google Gemini API key

## Installation

1. Clone the repository
2. Create `.env` file with your API key:
   ```bash
   cp .env.example .env
   ```
3. Add your API key to `.env`:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Running the App

Using `uv`:

```bash
uv run streamlit run src/app.py
```

Or install dependencies first:

```bash
uv sync
uv run streamlit run src/app.py
```

## Project Structure

```
quen-chatbot/
├── .streamlit/
│   └── config.toml      # Dark theme configuration
├── src/
│   ├── __init__.py
│   ├── app.py           # Streamlit UI application
│   └── gemini_client.py # Gemini API client
├── .env                 # API keys (gitignored)
├── .env.example         # Example environment file
├── .gitignore
├── pyproject.toml       # Project dependencies
└── README.md
```

## Getting a Gemini API Key

1. Visit [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Create a new API key
4. Add it to your `.env` file

## Customization

### Change the AI Model

Edit `src/app.py` and modify the model name in the `GeminiClient` initialization:

```python
st.session_state.client = GeminiClient(api_key=api_key, model_name="gemini-1.5-pro")
```

### Adjust Theme Colors

Edit `.streamlit/config.toml` to customize colors.
