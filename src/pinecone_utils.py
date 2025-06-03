#import uuid
from pinecone import Pinecone
from openai_utils import GenerateEmbeddings, OpenAIEmbeddingClient

def PineconeIndexClient(api_key, environment, index_name):
    if not all([api_key, environment, index_name]):
        raise ValueError("Faltam informações para conectar ao Pinecone.")

    pc = Pinecone(api_key=api_key)

    # Verifica se o índice existe
    if index_name not in pc.list_indexes().names():
        raise ValueError(f"Index '{index_name}' não existe no Pinecone.")

    # Retorna o cliente do índice
    return pc.Index(index_name)

def IngestEmbeddingsToPinecone(data, doc_embeds, index, namespace):
    for d, e in zip(data, doc_embeds):
        index.upsert(
            vectors=[{
            "id": d['id'],
            "values": e,
            "metadata": {'text': d['text']}
            }],
            namespace=namespace
        )
