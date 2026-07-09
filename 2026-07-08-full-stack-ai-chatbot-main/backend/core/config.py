import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///./chatbot.db")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

# print(f"DATABASE_URL: {DATABASE_URL}")
# print(f"OPENAI_API_KEY: {OPENAI_API_KEY}")