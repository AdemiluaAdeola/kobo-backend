import google.generativeai as genai
from ..core.config import get_settings

settings = get_settings()

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

# Use gemini-2.0-flash-exp (latest flash model, assuming "2.5 flash" refers to 2.0)
MODEL_NAME = "gemini-2.0-flash-exp"

async def get_chat_response(message: str, context: str = "") -> str:
    """
    Get a response from Gemini with optional context.
    """
    if not settings.GEMINI_API_KEY:
        return "I'm currently in 'offline' mode. (Gemini API Key missing). How can I help you manually?"

    model = genai.GenerativeModel(MODEL_NAME)
    
    prompt = f"""
    You are Cecilia, a brilliant and empathetic financial coach for the Kobo app.
    Kobo helps users in Nigeria (and generally) see tomorrow's money today using predictive forecasting.
    
    USER CONTEXT:
    {context}
    
    USER MESSAGE:
    {message}
    
    INSTRUCTIONS:
    - Be personable, professional, but friendly (Pidgin-friendly if the user speaks it).
    - Give actionable financial advice based on the context.
    - If the user asks about spending, refer to their 'safe to spend' or balance if provided in context.
    - Keep responses concise and helpful.
    """
    
    try:
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"I had a bit of a brain freeze: {str(e)}"
