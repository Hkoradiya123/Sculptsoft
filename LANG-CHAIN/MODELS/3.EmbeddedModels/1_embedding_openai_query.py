from langchain_openai import OpenAIEmbeddings   
from dotenv import load_dotenv

load_dotenv()

# Ensure OPENAI_API_KEY is in your .env file
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-large",
    dimensions = 32 # dimensions of the embedding vector means the length of the vector
)

result = embeddings.embed_query("What is the capital of India?")
print(result)
