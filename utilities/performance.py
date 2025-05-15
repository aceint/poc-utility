import time
import json
import numpy as np
import hnswlib
import psutil
import os
from typing import List, Dict, Optional

# --- Configuration ---
HNSWLIB_INDEX_PATH = '.\Data\hnswlib_index.bin'
CHROMA_COLLECTION_NAME = "text_embeddings"  # Changed to "text_embeddings"
DATA_FILE = ".\Data\embeddings.json"
QUERY_COUNT = 100
K = 10

def load_data(filename: str = DATA_FILE) -> List[Dict]:
    """Loads data from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"Loaded {len(data)} items from {filename}")
        return data
    except FileNotFoundError:
        print(f"Warning: Data file '{filename}' not found. Returning empty data.")
        return []

def create_hnsw_index(embeddings: List[List[float]], dim: int) -> hnswlib.Index:
    """Creates and initializes the HNSWlib index."""
    print(f"Creating HNSW index with dimension: {dim}")
    print(f"Number of embeddings: {len(embeddings)}")
    if embeddings:
        print(f"Shape of first embedding: {np.array(embeddings[0]).shape}")
    p = hnswlib.Index(space='l2', dim=dim)
    p.init_index(max_elements=len(embeddings), ef_construction=200, M=16)
    p.add_items(np.array(embeddings), list(range(len(embeddings))))
    return p

def load_hnsw_index(index_path: str, dim: int) -> hnswlib.Index:
    """Loads the HNSWlib index from a file."""
    p = hnswlib.Index(space='l2', dim=dim)
    try:
        p.load_index(index_path)
        return p
    except RuntimeError:
        raise RuntimeError(f"HNSWlib index file not found at {index_path}")

def generate_random_query_vectors(num_queries: int, dim: int) -> np.ndarray:
    """Generates a set of random query vectors."""
    return np.random.rand(num_queries, dim).astype(np.float32)

def measure_query_time(index: hnswlib.Index, query_vectors: np.ndarray, k: int) -> float:
    """Measures the average query time for a set of query vectors."""
    start_time = time.time()
    for vector in query_vectors:
        index.knn_query(vector, k=k)
    end_time = time.time()
    return (end_time - start_time) / len(query_vectors)

def get_memory_usage() -> float:
    """Gets the current memory usage of the process in MB."""
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss / (1024 * 1024)

def get_index_size(index_path: str) -> float:
    """Gets the size of the index file in MB."""
    if os.path.exists(index_path):
        return os.path.getsize(index_path) / (1024 * 1024)
    else:
        return 0.0


def main():
    """Main function to run the performance tests."""
    data = load_data()
    if not data:
        print("No data loaded.  Please ensure your data file is available.")
        return

    embeddings = []
    ids = []
    metadatas = []
    for i, item in enumerate(data):
        if 'embedding' in item:
            embeddings.append(item['embedding'])
            item_id_str = str(item['id'])  # Ensure ID is a string
            ids.append(item_id_str)
            metadatas.append({"id": item_id_str})  #  metadata
        else:
            print("Warning: An item in the data is missing the 'embedding' key. Skipping it.")
            print("Here is the item:")
            print(item)

    if not embeddings:
        print("No data with 'embedding' key found.  Cannot create HNSW or Chroma index.")
        return

    embedding_dim = len(embeddings[0])
    print(f"Number of valid embeddings found: {len(embeddings)}")
    print(f"Embedding dimension: {embedding_dim}")

    query_vectors = generate_random_query_vectors(QUERY_COUNT, embedding_dim)

    # --- HNSWlib Performance ---
    print("\n--- HNSWlib Performance ---")
    hnsw_index = create_hnsw_index(embeddings=embeddings, dim=embedding_dim)
    memory_usage_before_hnsw = get_memory_usage()
    average_query_time_hnsw = measure_query_time(hnsw_index, query_vectors, K)
    memory_usage_after_hnsw = get_memory_usage()
    index_size_hnsw = get_index_size(HNSWLIB_INDEX_PATH)

    print(f"Average query time ({QUERY_COUNT} queries, k={K}): {average_query_time_hnsw:.6f} seconds")
    print(f"Memory usage before HNSW query: {memory_usage_before_hnsw:.2f} MB")
    print(f"Memory usage after HNSW query: {memory_usage_after_hnsw:.2f} MB")
    print(f"HNSWlib index size: {index_size_hnsw:.2f} MB")

    # --- ChromaDB Performance ---
    print("\n--- ChromaDB Performance ---")
    try:
        import chromadb
        from chromadb.utils import embedding_functions

        client = chromadb.Client()
        collection = client.get_or_create_collection(CHROMA_COLLECTION_NAME)
        collection.add(
            embeddings=embeddings,
            ids=ids,
            metadatas=metadatas,
        )

        memory_usage_before_chroma = get_memory_usage()
        start_time_chroma = time.time()
        for query_vector in query_vectors:
            collection.query(query_embeddings=query_vector.tolist(), n_results=K)
        end_time_chroma = time.time()
        average_query_time_chroma = (end_time_chroma - start_time_chroma) / QUERY_COUNT
        memory_usage_after_chroma = get_memory_usage()
        index_size_chroma = 0

        print(f"Average query time ({QUERY_COUNT} queries, k={K}): {average_query_time_chroma:.6f} seconds")
        print(f"Memory usage before Chroma query: {memory_usage_before_chroma:.2f} MB")
        print(f"Memory usage after Chroma query: {memory_usage_after_chroma:.2f} MB")
        print(f"ChromaDB index size: {index_size_chroma:.2f} MB (Approximation)")

    except ImportError:
        print("ChromaDB is not installed. Please install it to run ChromaDB performance tests.")
    except Exception as e:
        print(f"Error running ChromaDB tests: {e}")



if __name__ == "__main__":
    main()
