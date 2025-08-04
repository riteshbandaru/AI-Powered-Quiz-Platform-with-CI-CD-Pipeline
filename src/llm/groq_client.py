from langchain_groq import ChatGroq
from src.config.settings import Settings

def groq_client():
    return ChatGroq(api_key=Settings.GROQ_API, model_name=Settings.MODEL, temperature=Settings.TEMPERATURE)
