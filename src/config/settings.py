import os
from dotenv import load_dotenv

load_dotenv()

class Settings:

    GROQ_API = os.getenv('GROQ_API')

    MODEL="llama-3.1-8b-instant"

    TEMPERATURE=0.9

    MAX_RETRIES=3   #This is for the max api calls if once an api call fails then these are the max retires