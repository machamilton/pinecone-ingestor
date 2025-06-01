import uuid
from pinecone import Pinecone

def PineconeIndexClient(api_key, environment, index_name):
    if not all([api_key, environment, index_name]):
        raise ValueError("Faltam informações para conectar ao Pinecone.")

    pc = Pinecone(api_key=api_key)

    # Verifica se o índice existe
    if index_name not in pc.list_indexes().names():
        raise ValueError(f"Index '{index_name}' não existe no Pinecone.")

    # Retorna o cliente do índice
    return pc.Index(index_name)

def IngestEmbeddingsToPinecone(
    index,
    embeddings,
    namespace
):
    """
    Insere os embeddings no índice Pinecone.
    Cada item precisa de um ID único.
    """
    vectors = []
    for item in embeddings:
        vector_id = str(uuid.uuid4())
        vector_data = {
            "id": vector_id,
            "values": item["embedding"],
            "metadata": {
                "text": item["text"]
            }
        }
        vectors.append(vector_data)

    # Pinecone espera uma lista de tuplas (id, vector, metadata)
    index.upsert(
        vectors=[
            (v["id"], v["values"], v["metadata"]) for v in vectors
        ],
        namespace=namespace
    )
