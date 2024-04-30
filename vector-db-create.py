#vector-db-create.py
# create a vector database from a pdf file

from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

# Initialize HuggingFaceEmbeddings
embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize PyPDFLoader with the path to the PDF file
loaders = [PyPDFLoader('.uhc/Medical Member Handbook starting 1_1_2024.pdf')]

# Load the PDF file
docs = []
for file in loaders:
    docs.extend(file.load())

# Split the text into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(docs)

# Use HuggingFaceEmbeddings to generate embeddings for the text chunks
# The embeddings are used to create a vectorstore
# The vectorstore is a database that stores the embeddings for each text chunk
# The persist_directory argument specifies where the vectorstore should be saved
vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory="./chroma_db_nccn")

# Print the number of documents in the vectorstore
# Each document corresponds to a text chunk
print(vectorstore._collection.count())
