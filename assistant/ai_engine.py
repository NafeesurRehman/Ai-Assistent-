
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

_client = None
_api_key = None
_model = "gemini-3.8-flash"


def configure_ai(api_key=None, model=None):

    global _client, _api_key, _model

    if api_key is None:
        api_key = os.getenv("GEMINI_API_KEY")

    if model:
        _model = model

    _api_key = api_key.strip() if api_key else None

    if _api_key:
        _client = genai.Client(api_key=_api_key)
    else:
        _client = None


def get_ai_response(message):

    if not _client:
        return "Gemini API key missing. Please configure it in Settings."

    try:
        response = _client.models.generate_content(
            model=_model,
            contents=message
        )

        return response.text or "AI returned an empty response."

    except Exception as error:

        print("\n========== GEMINI ERROR ==========")
        print(type(error).__name__)
        print(str(error))
        print("==================================\n")

        return "Gemini connection failed. Check terminal."
        

configure_ai()