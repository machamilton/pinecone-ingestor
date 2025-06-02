from data_loading import DataLoader
from preprocess import ConvertToMarkdown, SplitDocuments
from openai_utils import OpenAIEmbeddingClient, GenerateEmbeddings
from pinecone_utils import PineconeIndexClient, IngestEmbeddingsToPinecone
import os
from dotenv import load_dotenv


if __name__ == "__main__":
    # Carrega variáveis de ambiente
    load_dotenv()
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT_REGION")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    PDF_PATH = os.getenv("PDF_PATH")
    PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE")

    print("🚀 Iniciando o pipeline de ingestão...")

    # 1. Carregar o PDF
    print("Carregando o PDF...")
    raw_documents = DataLoader(PDF_PATH)

    # 2. Converter para Markdown enriquecido
    print("Convertendo para Markdown...")
    markdown_documents = ConvertToMarkdown(raw_documents)

    # 3. Split em chunks
    print("Dividindo em chunks...")
    chunks = SplitDocuments(markdown_documents)

    # 4. Gerar embeddings com OpenAI
    print("Gerando embeddings...")
    client = OpenAIEmbeddingClient(OPENAI_API_KEY)
    embeddings = GenerateEmbeddings(client, ([d["text"] for d in chunks]))
    

    # 5. Ingestão no Pinecone
    print("Enviando para Pinecone...")
    index = PineconeIndexClient(PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME)
    IngestEmbeddingsToPinecone(chunks, embeddings, index, PINECONE_NAMESPACE)

    print("Pipeline finalizado com sucesso!")
