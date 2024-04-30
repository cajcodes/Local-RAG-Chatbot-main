#vector-db-create.py
# create a vector database from a pdf file

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize HuggingFaceEmbeddings
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

loaders = [PyPDFLoader('.uhc/Medical Member Handbook starting 1_1_2024.pdf')]

docs = []
for file in loaders:
    docs.extend(file.load())

# Split text to chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# Use HuggingFaceEmbeddings for generating embeddings
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_nccn")

print(vectorstore._collection.count())
