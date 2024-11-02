import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import normalize

def load_json(file_path):
    """Load data from a JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_traceability(class_vectors, requirement_vectors, threshold=0.7):
    """Find traceability between class implementations and requirements."""
    traceability = {}

    # Normalize class and requirement vectors to unit length
    class_vectors_normalized = {k: normalize([v])[0] for k, v in class_vectors.items()}
    requirement_vectors_normalized = {k: normalize([v])[0] for k, v in requirement_vectors.items()}

    # Iterate over each requirement and its vector
    for req_name, req_vector in requirement_vectors_normalized.items():
        traceability[req_name] = []
        print(f"Processing requirement: {req_name}")  # Print current requirement
        
        # Calculate similarity with each class vector
        for class_name, class_vector in class_vectors_normalized.items():
            print(f"  Comparing with class: {class_name}")  # Print current class
            similarity = cosine_similarity([req_vector], [class_vector])[0][0]
            
            # Check if similarity exceeds the threshold
            if similarity >= threshold:
                traceability[req_name].append((class_name, similarity))
                print(f"    Found match: {class_name} with similarity {similarity:.2f}")  # Print matched class

    return traceability

if __name__ == "__main__":
    # Load class and requirement vector indexes
    class_vector_index = load_json("class_vector_index.json")  # Change as necessary
    requirement_vector_index = load_json("requirement_vector_index.json")

    # Find traceability between requirements and class implementations
    traceability_results = find_traceability(class_vector_index, requirement_vector_index, threshold=0.7)

    # Print or save the traceability results
    with open("traceability_results.json", "w", encoding="utf-8") as f:
        json.dump(traceability_results, f, indent=4)

    print("Traceability analysis complete. Results saved as traceability_results.json.")
