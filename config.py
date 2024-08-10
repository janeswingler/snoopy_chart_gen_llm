import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENAI_API_KEY')
if API_KEY is None:
    raise ValueError("No OPENAI_API_KEY found in environment variables")