from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
from typing import TypedDict,Annotated  
import os   
from pydantic import Field,BaseModel
from typing import Literal,Optional
load_dotenv()   

model = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-3.5-turbo",
    temperature=0.7,
)

chat_model = ChatOpenAI(llm=model)

class Review(BaseModel):
    key_themes: list[str] = Field(description="List of key themes in the review")
    summary: str = Field(description="A brief summary of the review")
    sentiment: Literal["positive","negative","neutral"] = Field(description="Overall sentiment of the review")
    pros: Optional[list[str]] = Field(description="List of pros")
    cons: Optional[list[str]] = Field(description="List of cons")   
    name: Optional[str] = Field(description="Name of the product")
    
structured_model = chat_model.with_structured_output(Review)        
    
result = structured_model.invoke(""" The hardware is great, but the sofware feels bloated. there are too many pre-installed apps that i can't remove. Hopinf for a software update to fix this""")

print(result)
print(result.summary)
print(result.sentiment)
print(result.name)
print(result.pros)
print(result.cons)
print(result.key_themes)
