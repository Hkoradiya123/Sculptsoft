from langchain_huggingface import HuggingFaceEmbeddings 
from dotenv import load_dotenv

load_dotenv()

# Ensure HUGGINGFACEHUB_API_TOKEN is in your .env file
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    
)

result = embeddings.embed_documents(["What is the capital of France?", "What is the capital of India?"])
print(result)

