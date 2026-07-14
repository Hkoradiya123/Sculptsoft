from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import PyPDFLoader

pdf = "LANGCHAIN_DOCUMENT_LOADERS/data_files/TASK - Hospital Case Management System (SQLAlchemy ORM).pdf"
loader = PyPDFLoader(pdf)

docs = loader.load()




splitter = CharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 10, # chunk_overlap is used to overlap 
)

result = splitter.split_documents(docs) # can use split_text for text files
print(result[0])