from langchain_community.document_loaders import WebBaseLoader
from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,    
)

model = ChatHuggingFace(llm = llm)

parser = StrOutputParser()



url = "https://www.amazon.in/ASUS-Gaming-5090-24GB-Windows-G835LX-SA187WS/dp/B0F5BFQR4T/ref=asc_df_B0F5BFQR4T?mcid=24f87c3ea43532d58f87c72a6df9b2b4&tag=googleshopdes-21&linkCode=df0&hvadid=709855510254&hvpos=&hvnetw=g&hvrand=9197121705590134825&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9061748&hvtargid=pla-2420433681976&psc=1&gad_source=1"
loader = WebBaseLoader(url)
data = loader.load()

prompt = PromptTemplate(
    template = "answer the following question \n {question} from the following content \n {content}",
    input_variables=["content","question"]
)

chain = prompt | model | parser

result = chain.invoke({"content":data[0].page_content,"question":"what is the price of this product"})
print(result)
