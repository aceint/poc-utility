import json
from chromadb import Client

# Initialize ChromaDB client
client = Client()

# Create or get a collection
collection = client.get_or_create_collection("text_embeddings")

# Load embeddings from JSON file
with open('embeddings.json', 'r') as f:
    embeddings_data = json.load(f)

# Add embeddings to the collection
for item in embeddings_data:
    try:
        # Ensure the ID is a string for ChromaDB
        item_id_str = str(item['id'])

        collection.add(
            ids=[item_id_str],  # <--- ADD THIS LINE
            documents=[f"Document ID: {item_id_str}"], # Using item_id_str here too for consistency
            embeddings=[item['embedding']],
            metadatas=[{"id": item_id_str}] # Using item_id_str here too, if it's an int convert it
        )
    except KeyError as e:
        print(f"KeyError: {e} for item: {item}")
    except Exception as e: # Catch other potential errors, especially after fixing the TypeError
        print(f"An error occurred with item {item.get('id', 'Unknown ID')}: {e}")
        # It might be useful to print the problematic embedding or its type
        if 'embedding' in item:
            print(f"Problematic embedding type: {type(item['embedding'])}, first few elements: {item['embedding'][:5]}")


print("Embeddings indexing process finished in ChromaDB.")