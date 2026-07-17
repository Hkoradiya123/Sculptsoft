from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFaceEndpoint,ChatHuggingFace
# from langchain_google_genai import GoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv
import os 

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id="meta-llama/Llama-3.1-8B-Instruct",
    task="text-generation",
    temperature=0.4,
    huggingfacehub_api_token=os.environ.get("HuggingFace_API_KEY")
)

model = ChatHuggingFace(llm = llm)

loader = PyPDFLoader(os.path.join(os.path.dirname(__file__), 'reader.pdf'))

docs = loader.load()

text = ""

for i in docs:
    text = text + i.page_content

splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap = 40)

chunk = splitter.create_documents([text])

embedding  = HuggingFaceEmbeddings(model_name = 'sentence-transformers/all-MiniLM-L6-v2')

vector_store = FAISS.from_documents(chunk, embedding)

retriever = vector_store.as_retriever(search_type='similarity', kwargs={'k':2})


prompt = PromptTemplate(
    template="""
    You are a helpful assistant.
    Answer ONLY from the provided transcript context.
    If the context is insufficient, just say you don't know.

    {context}
    Question: {question}
    """,
    input_variables=['context', 'question']
)

# model = GoogleGenerativeAI(model= 'gemini-1.5-flash')

parser = StrOutputParser()

def format_doc(retriever_doc):
    return '\n\n'.join(document.page_content for document in retriever_doc)

retriever_chain = RunnableParallel({
    'context': retriever | RunnableLambda(format_doc),
    'question' : RunnablePassthrough()
})

generation_chain = retriever_chain | prompt | model | parser

response = generation_chain.invoke('what is Hospital Case Management System ')

print(response)