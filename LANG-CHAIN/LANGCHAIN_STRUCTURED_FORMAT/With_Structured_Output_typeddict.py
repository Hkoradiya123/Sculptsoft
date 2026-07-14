from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
from typing import TypedDict,Annotated  
import os   
load_dotenv()

model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo",
    temperature=0.7,
)

chat_model = ChatOpenAI(llm=model)

class Review(TypedDict):
    summary : Annotated[str,"A brief summary of the review"]
    sentiment : Annotated[str,"The sentiment of the review (positive, negative, neutral)"]
structured_model = chat_model.with_structured_output(Review)        
    
result = structured_model.invoke(""" The hardware is great, but the sofware feels bloated. there are too many pre-installed apps that i can't remove. Hopinf for a software update to fix this""")

print(result)
print(result["summary"])
print(result["sentiment"])
