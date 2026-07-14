from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-V3.2",
    task="text-generation",
    temperature=1.2, # if we put temperature near 0 or  0 then it will give us the same output every time,if we put temperature 1-2 then it will give us different output every time
)

chat_model = ChatHuggingFace(llm=llm)

result = chat_model.invoke("write 5 line poem on football")
print(result.content)