import json
import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch

# Load model and tokenizer
model_name = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

# Generate embeddings
embeddings = []
for item in data:
    inputs = tokenizer(item['text'], return_tensors='pt', padding=True, truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings.append(outputs.last_hidden_state.mean(dim=1).numpy())

# Convert to numpy array
embeddings = np.array(embeddings).squeeze()

# Save embeddings and metadata to a new JSON file
output_data = [{"id": item['id'], "embedding": embedding.tolist()} for item, embedding in zip(data, embeddings)]
with open('embeddings.json', 'w') as f:
    json.dump(output_data, f)

print("Embeddings generated and saved to embeddings.json")
