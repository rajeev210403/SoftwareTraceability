import os
import json
from transformers import BertTokenizer, BertModel
import torch

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def vectorize_text(text):
    """Tokenize and generate BERT embeddings for a given text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    return embeddings.tolist()

def vectorize_requirements(requirements_dir):
    """Vectorize all requirements in the specified directory."""
    vector_index_requirements = {}

    # Process each requirement file in the directory
    for req_file in os.listdir(requirements_dir):
        if req_file.endswith(".txt"):
            req_file_path = os.path.join(requirements_dir, req_file)
            
            # Read and vectorize the content of the requirement file
            with open(req_file_path, 'r', encoding='utf-8') as f:
                requirement_text = f.read()
            
            print(f"Vectorizing requirement: {req_file}")
            vector_index_requirements[req_file] = vectorize_text(requirement_text)

    return vector_index_requirements

if __name__ == "__main__":
    requirements_dir = "./datasets/iTrust/req"  # Directory containing requirement text files
    requirements_vector_index = vectorize_requirements(requirements_dir)

    # Save the requirements vector index to a JSON file
    with open("requirement_vector_index.json", "w", encoding="utf-8") as f:
        json.dump(requirements_vector_index, f, indent=4)

    print("Requirement vector indexing complete. File saved as requirement_vector_index.json.")
