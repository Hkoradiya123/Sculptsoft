from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()



text_splitter = SemanticChunker(
    OpenAIEmbeddings(),
    breakpoint_threshold_type = "standard_deviation",
    breakpoint_threshold_amount = 2,
    )

sample_text = """
farmers are very important to a country , they provide food to the country and also provide employment to the country.
cristiano ronaldo is the best player in the world. nasa is the a space agency of the United States of America.
"""

result = text_splitter.create_documents([sample_text])  
print(result)
print(len(result))