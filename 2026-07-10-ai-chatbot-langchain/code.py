from langchain_openai import ChatOpenAI  # 1. Import OpenAI wrapper
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# 1. Model — Replace ChatAnthropic with ChatOpenAI
# Ensure OPENAI_API_KEY is set in your environment variables


model = ChatOpenAI(
    model="gpt-5-mini",
    max_completion_tokens=500, 
    timeout=30,                                            
    max_retries=2,              
)

# 2. Prompt template 
prompt = []


# 3. Output parser — Same as before
parser = StrOutputParser()

# 4. LCEL chain — Same pipe syntax
chain = prompt | model | parser

# 5. Run — Same invoke method



for chunk in chain.stream({"topic": "database connection pooling"}):
    print(chunk, end="", flush=True)