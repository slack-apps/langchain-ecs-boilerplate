from dotenv import load_dotenv
from langchain.document_loaders import DirectoryLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS

load_dotenv()

DOCS_DIR = '.docs'
DB_DIR = '.db'


def create_vectorstore_index():
    embeddings = OpenAIEmbeddings()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)

    loader = DirectoryLoader(DOCS_DIR, glob="*.txt")
    docs = loader.load()
    sub_docs = text_splitter.split_documents(docs)

    vectorstore = FAISS.from_documents(documents=sub_docs, embedding=embeddings)

    vectorstore.save_local(folder_path=DB_DIR)


if __name__ == '__main__':
    create_vectorstore_index()
