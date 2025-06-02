import re
from langchain.text_splitter import RecursiveCharacterTextSplitter
import uuid

def ConvertToMarkdown(documents):
    """
    Converte os documentos (langchain Document) para Markdown enriquecido:
    - Títulos (linhas com tudo em maiúsculo e >10 caracteres) recebem '##'
    - Listas com traço ou número são formatadas corretamente
    - Espaços e quebras de linha são limpos
    """
    markdown_docs = []

    for doc in documents:
        content = doc.page_content

        # Limpeza de espaços excessivos
        content = re.sub(r'\s+\n', '\n', content)
        content = re.sub(r'\n{3,}', '\n\n', content)

        lines = content.split('\n')
        markdown_lines = []

        for line in lines:
            stripped = line.strip()

            # Títulos: linha em maiúsculas com mais de 10 caracteres
            if stripped.isupper() and len(stripped) > 10:
                markdown_lines.append(f'## {stripped.capitalize()}')
            # Listas com traço
            elif re.match(r'^[-–•]\s+', stripped):
                markdown_lines.append(f'- {stripped[2:].strip()}')
            # Listas numeradas
            elif re.match(r'^\d+\.\s+', stripped):
                markdown_lines.append(f'{stripped}')
            else:
                markdown_lines.append(stripped)

        markdown_doc = '\n'.join(markdown_lines).strip()
        markdown_docs.append(markdown_doc)

    return markdown_docs


def SplitDocuments(markdown_documents, chunk_size=500, chunk_overlap=100):
    """
    Divide os textos Markdown em chunks com sobreposição, prontos para embeddings.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for text in markdown_documents:
        splits = splitter.split_text(text)
        for split in splits:
            dic_return = {}
            dic_return["id"] = str(uuid.uuid4())
            dic_return["text"] = split
            chunks.append(dic_return)
        
    return chunks
