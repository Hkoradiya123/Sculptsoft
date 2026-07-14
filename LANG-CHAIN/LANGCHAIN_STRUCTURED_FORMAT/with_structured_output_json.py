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

json_schema = {
    "title":"Review",
    "description":"A review of a product",
    "type":"object",
    "properties":{
        "name":{
            "type":"string"
        },
        "sentiment":{
            "type":"string"
        },
        "pros":{
            "type":"array",
            "items":{
                "type":"string"
            }
        },
        "cons":{
            "type":"array",
            "items":{
                "type":"string"
            }
        }
    },  
    "required":["key_themes","summary","sentiment","pros","cons","name"]
}   

structured_model = chat_model.with_structured_output(json_schema)        
    
result = structured_model.invoke(""" The hardware is great, but the sofware feels bloated. there are too many pre-installed apps that i can't remove. Hopinf for a software update to fix this""")

print(result)
print(result["summary"])
print(result["sentiment"])
print(result["name"])
print(result["pros"])
print(result["cons"])
print(result["key_themes"])
    