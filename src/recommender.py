import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

with open('C:\\Users\\HP\\Desktop\\vscode\\BookSnap\\Book\\data\\ocr_results\\ocr_output.json', 'r') as f:
    ocr_data = json.load(f)

# Simulate descriptions from OCR words
descriptions = []
image_keys = []
for key, word_list in ocr_data.items():
    if word_list:
        simulated_description = " ".join(word_list)
        descriptions.append(simulated_description)
        image_keys.append(key)

# Generate embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(descriptions)

# Compute similarity matrix
similarity_matrix = cosine_similarity(embeddings)

# Build recommendations
recommendations = {}
for i, key in enumerate(image_keys):
    scores = list(enumerate(similarity_matrix[i]))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    top_matches = [image_keys[j] for j, score in scores[1:4]]
    recommendations[key] = top_matches

# Save recommendations
with open('C:\\Users\\HP\\Desktop\\vscode\\BookSnap\\Book\\data\\ocr_results\\recommendations.json', 'w') as f:
    json.dump(recommendations, f, indent=2)
