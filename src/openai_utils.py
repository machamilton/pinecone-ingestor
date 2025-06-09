from openai import OpenAI
from typing import List

def OpenAIEmbeddingClient(api_key):
    """
    Retorna um cliente OpenAI configurado com a chave da API.
    """
    api_key = api_key
    if not api_key:
        raise ValueError("A chave da API OpenAI não foi fornecida.")

    client = OpenAI(api_key=api_key)
    return client


def GenerateEmbeddings(client, embedding_model, docs: list[str]) -> list[list[float]]:
    res = client.embeddings.create(
        input=docs,
        model=embedding_model
    )
    doc_embeds = [r.embedding for r in res.data] 
    return doc_embeds 


'''
def LegacyGenerateEmbeddings(text_chunks: List[str], client, model: str = "text-embedding-3-small"):
    """
    Gera embeddings para uma lista de textos usando o modelo da OpenAI.
    """
    embeddings = []
    for text in text_chunks:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        vector = response.data[0].embedding
        embeddings.append({
            "text": text,
            "embedding": vector
        })
    return embeddings
'''