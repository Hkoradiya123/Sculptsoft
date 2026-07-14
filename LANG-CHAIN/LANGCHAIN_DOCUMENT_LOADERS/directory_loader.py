from langchain_community.document_loaders import DirectoryLoader,PyPDFLoader

loader = DirectoryLoader(
    path = "LANGCHAIN_DOCUMENT_LOADERS/books",
    glob = "*.pdf", # it will load all the pdf files from the directory
    # | Glob Pattern |            What it Loads                        |
    # |------------- |--------------------------------------|
    # | */.txt       | All .txt files in all subfolders     |
    # | *.pdf        | All .pdf files in the root directory |
    # | data/*.csv   | All .csv files in the data/ folder   |
    # | */           | All files (any type, all folders)    |
    loader_cls = PyPDFLoader
)
data = loader.lazy_load() # lazy load is used to load the documents one by one in memory it is used to save the memory
# lazy load runs faster than load function.

# use lazy load when there are large number of documents to load

for document in data:
    print(document.metadata)
