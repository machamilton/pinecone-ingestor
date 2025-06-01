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

def chunked(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def IngestEmbeddingsToPinecone(index, embeddings, namespace, batch_size=100):
    for batch_num, batch in enumerate(chunked(embeddings, batch_size)):
        records = [
            {
                "id": f"{namespace}_doc_{batch_num}_{i}",
                "values": emb
            }
            for i, emb in enumerate(batch)
        ]
        index.upsert_records(namespace, records)
        print(f"[Pinecone] Batch {batch_num + 1} uploaded with {len(batch)} vectors.")
