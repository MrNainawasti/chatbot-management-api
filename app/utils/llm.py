from google import genai
from app.core.config import settings

client = genai.Client(api_key=settings.GEMINI_API_KEY)

def generate_ai_response(prompt: str, model_name:str = "gemini-3.5-flash") -> str:
    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt
        )
        return response.text
    except Exception as e:
        print(f"LLM Error: {e}")
        return "Sorry I ran into error generating a response"
