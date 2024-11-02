import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def load_json(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def normalize_vectors(vectors):
    """Normalize a list of vectors."""
    return np.array([vector / np.linalg.norm(vector) if np.linalg.norm(vector) > 0 else vector for vector in vectors])

# Load vectorized requirements, code summaries, and keywords
vectorized_requirements = load_json("requirement_vector_index.json")  # Your requirements vector file
vectorized_summaries = load_json("code_summary_indexing.json")  # Your summaries vector file
vectorized_keywords = load_json("vector_index.json")  # Your keywords vector file

# Initialize the mapping dictionary
requirement_to_classes_mapping = {}

# Normalize the keyword and summary vectors
normalized_summaries = {k: normalize_vectors([v])[0] for k, v in vectorized_summaries.items()}
normalized_keywords = {k: normalize_vectors([v])[0] for k, v in vectorized_keywords.items()}

# Calculate the similarity and create mappings
for req_name, req_vector in vectorized_requirements.items():
    print(f"Processing requirement: {req_name}")  # Print current requirement
    
    # Initialize a list to hold classes that meet the similarity threshold
    mapped_classes = {}

    for class_name, class_vector in normalized_summaries.items():
        # Compute cosine similarity with summaries
        similarity_summary = cosine_similarity([req_vector], [class_vector])[0][0]
        
        # Compute cosine similarity with keywords if they exist
        similarity_keyword = 0
        if class_name in normalized_keywords:
            keyword_vector = normalized_keywords[class_name]
            similarity_keyword = cosine_similarity([req_vector], [keyword_vector])[0][0]

        # Aggregate the similarities
        final_similarity_score = (similarity_summary + similarity_keyword) / 2  # Simple average, adjust as needed

        # Define a threshold for what constitutes a "similar" mapping
        threshold = 0.7  # Adjust this threshold as needed

        if final_similarity_score >= threshold:
            mapped_classes[class_name] = final_similarity_score  # Store class with its score

    # Store the mapping for the current requirement
    requirement_to_classes_mapping[req_name] = mapped_classes

# Save the mapping to a JSON file
with open("requirement_to_classes_mapping.json", "w", encoding="utf-8") as f:
    json.dump(requirement_to_classes_mapping, f, indent=4)

print("Mapping of requirements to classes complete. File saved as requirement_to_classes_mapping.json.")
