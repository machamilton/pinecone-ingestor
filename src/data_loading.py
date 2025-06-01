from langchain_community.document_loaders import PyPDFLoader

def DataLoader(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    return docs