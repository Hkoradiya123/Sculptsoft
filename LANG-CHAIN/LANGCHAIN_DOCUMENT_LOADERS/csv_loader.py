from langchain_community.document_loaders import CSVLoader
loader = CSVLoader(file_path = "LANGCHAIN_DOCUMENT_LOADERS/data_files/raw_sales_data.csv")
data = loader.load()

print(len(data))
print(data[0])
