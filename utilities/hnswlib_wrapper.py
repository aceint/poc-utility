import hnswlib
import json
import numpy as np

# Load embeddings from JSON file
with open('embeddings.json', 'r') as f:
    embeddings_data = json.load(f)

# Extract the embedding vectors from the list of dictionaries
embeddings_list = [item['embedding'] for item in embeddings_data]

# Convert the list of embedding vectors to a NumPy array
embeddings_array = np.array(embeddings_list)

# Initialize HNSWlib index
dim = embeddings_array.shape[1]  # Dimension of the embeddings
num_elements = len(embeddings_array)

# Create the index
p = hnswlib.Index(space='l2', dim=dim)
p.init_index(max_elements=num_elements, ef_construction=200, M=16)

# Add embeddings to the index
p.add_items(embeddings_array, list(range(num_elements)))

# Set the ef for querying
p.set_ef(50)  # ef should be > k

# Save the index to a file
index_path = 'hnswlib_index.bin'
p.save_index(index_path)

print(f"HNSWlib index saved to: {index_path}")

# To load the index later:
# loaded_index = hnswlib.Index(space='l2', dim=dim)
# loaded_index.load_index(index_path)
# loaded_index.set_ef(50) # Remember to set ef for querying after loading