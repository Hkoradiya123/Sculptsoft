import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

# | Use Case                         | Recommended Loader                              |
# |----------------------------------|-------------------------------------------------|
# | Simple, clean PDFs               | PyPDFLoader                                     |
# | PDFs with tables/columns         | PDFPlumberLoader                                |
# | Scanned/image PDFs               | UnstructuredPDFLoader or AmazonTextractPDFLoader|
# | Need layout and image data       | PyMuPDFLoader                                   |
# | Want best structure extraction   | UnstructuredPDFLoader                           |

# detailed code for all the above mentioned loaders :- https://docs.langchain.com/oss/python/integrations/document_loaders#pdfs

# Ye file ke relative path ko resolve karta hai, chahe kahi se bhi script run karo
pdf_path = Path(__file__).parent / "data_files" / "Task.pdf"
loader = PyPDFLoader(str(pdf_path))
data = loader.load()
print(data)
print(len(data))
print(data[0].page_content)
print(data[0].metadata)