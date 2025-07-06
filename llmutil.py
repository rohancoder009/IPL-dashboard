import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load .env if not running inside Streamlit
load_dotenv()

def setup_gemini(api_key=None):
    if api_key is None:
        api_key = os.getenv("API_KEY")  # fallback for CLI/local
    genai.configure(api_key=api_key)

def _gemini_summary(prompt):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {str(e)}"

def summarize_stats(prompt):
    return _gemini_summary(prompt)
