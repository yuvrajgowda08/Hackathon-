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
    
def search(query_embedding, k=3):

    global index
    global chunks

    distances, indices = index.search(
        np.array([query_embedding]),
        k
    )

    results = [chunks[i] for i in indices[0]]

    return results