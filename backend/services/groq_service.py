from groq import Groq
from backend.config import GROQ_API_KEY

_client = None


def _get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def ask_groq(system_msg: str, user_msg: str) -> str:
    try:
        resp = _get_client().chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def get_short_tip(items: list[str]) -> str:
    return ask_groq(
        "You are an Environmental Waste Management Expert. Give a short 2-3 sentence professional tip about proper disposal or recycling.",
        f"Detected waste: {', '.join(i.replace('_', ' ') for i in items)}. Quick recommendation?",
    )


def get_deep_explanation(items: list[str]) -> str:
    return ask_groq(
        "You are a professional Waste Management Expert. Explain in structured format: "
        "1) Category 2) Why 3) Disposal steps 4) Environmental impact 5) Safety 6) Sustainability tips",
        f"Detected: {', '.join(i.replace('_', ' ') for i in items)}. Explain in detail.",
    )


def chat_response(user_message: str) -> str:
    return ask_groq(
        "You are a professional Waste Management Assistant. Provide detailed, clear, "
        "educational explanations about waste disposal, recycling, hazardous waste, and environmental impact.",
        user_message,
    )
