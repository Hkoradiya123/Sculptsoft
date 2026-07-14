from langchain_huggingface import HuggingFaceEmbeddings 
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import os
load_dotenv()



embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
)

documents = [
    "cristiano ronaldo is the best player in the world",
    "messi is the 2nd best player in the world",
    "neymar is the 3rd best player in the world",
    "maradona is the 4th best player in the world",
    "pele is the 5th best player in the world"
    " new gen player mbappe is the best"
]

query = "2nd best?"
doc_embeddings = embeddings.embed_documents(documents)
query_embedding = embeddings.embed_query(query)

cosine_similarities = cosine_similarity([query_embedding], doc_embeddings)[0] # both should be 2d list, and we need best match so we take 0th index

index,scores = sorted(list(enumerate(cosine_similarities)), key=lambda x: x[1])[-1]
print("User Query is ")
print(query)
print("Answer:")
print(documents[index])
print("similarity score is ", scores)
