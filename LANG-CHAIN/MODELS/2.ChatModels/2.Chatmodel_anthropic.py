from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

load_dotenv()

# Ensure ANTHROPIC_API_KEY is in your .env file
model = ChatAnthropic(model="claude-3-opus-20240229")

result = model.invoke("What is the capital of France?")
print(result.content)
