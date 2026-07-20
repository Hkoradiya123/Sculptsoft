from dotenv import load_dotenv
load_dotenv()
from rag import retrieve
docs = retrieve('contect number of hr', k=6)
if not docs:
    print('NO DOCS RETURNED')
for d in docs:
    print('---')
    print(d.metadata)
    print(d.page_content[:300])