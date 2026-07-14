from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

# Ensure HUGGINGFACEHUB_API_TOKEN is in your .env file
# free and open source model
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
)

chat_model = ChatHuggingFace(llm=llm)

result = chat_model.invoke("What is the capital of India?")
print(result.content)