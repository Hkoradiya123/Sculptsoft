from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

file_path = "LANGCHAIN_DOCUMENT_LOADERS/data_files/example.txt"

loader = TextLoader(file_path,encoding = "utf-8")
data = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap = 0,
)

chunks = splitter.split_documents(data)
print(chunks[0])
print(len(chunks))


