import faiss
import numpy as np

index = None
chunks = []


def build_vector_store(embeddings, texts):

    global index
    global chunks

    dimension = len(embeddings[0])

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    chunks = texts


def search(query_embedding, k=3):

    global index
    global chunks

    distances, indices = index.search(
        np.array([query_embedding]),
        k
    )

    results = [chunks[i] for i in indices[0]]

    return results