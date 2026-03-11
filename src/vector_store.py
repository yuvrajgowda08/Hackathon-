import faiss
import numpy as np

index = None
chunks = []


def build_vector_store(embeddings, chunks):

    global index
    global documents

    if len(embeddings) == 0:
        return

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    documents = chunks

def search(query_embedding, top_k=3):

    global index
    global chunks

    if index is None or len(chunks) == 0:
        return []

    distances, indices = index.search(
        np.array([query_embedding]),
        min(top_k, len(chunks))
    )

    results = []

    for i in indices[0]:
        if i >= 0 and i < len(chunks):
            results.append(chunks[i])

    return results