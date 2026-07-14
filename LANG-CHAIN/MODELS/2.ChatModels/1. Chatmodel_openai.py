from langchain_openai import ChatOpenAI     
from dotenv import load_dotenv

load_dotenv()

model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7,max_completion_tokens=100) # temperature controls the creativeness of the output,temperture :- (0,2)
# max_completion_tokens controls the maximum number of tokens to generate

result = model.invoke("What is the capital of France?")
print(result.content)   
