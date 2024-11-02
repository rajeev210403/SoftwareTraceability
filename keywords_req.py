import os
import json

# Define a set of common English stop words
stop_words = set([
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "what", "which", "who", "whom", "this",
    "that", "these", "those", "am", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to",
    "from", "up", "down", "in", "out", "on", "off", "over", "under", "again",
    "further", "then", "once", "here", "there", "when", "where", "why", "how",
    "all", "any", "both", "each", "few", "more", "most", "other", "some",
    "such", "no", "nor", "not", "only", "own", "same", "so", "than", "too",
    "very", "s", "t", "can", "will", "just", "don", "should", "now"
])

def extract_keywords(text):
    """Extract keywords from the given text, removing stop words."""
    if text:  # Check if text is not None or empty
        return list(set(word for word in text.split() if word.lower() not in stop_words))
    return []  # Return an empty list if text is None or empty

def extract_keywords_from_requirements(requirements_dir):
    """Extract keywords from all requirement files in the specified directory."""
    keywords_index = {}

    # Process each requirement file in the directory
    for req_file in os.listdir(requirements_dir):
        if req_file.endswith(".txt"):
            req_file_path = os.path.join(requirements_dir, req_file)
            
            # Read the content of the requirement file
            with open(req_file_path, 'r', encoding='utf-8') as f:
                requirement_text = f.read()
            
            print(f"Extracting keywords from requirement: {req_file}")
            keywords_index[req_file] = extract_keywords(requirement_text)

    return keywords_index

if __name__ == "__main__":
    requirements_dir = "./datasets/iTrust/req"  # Directory containing requirement text files
    requirements_keywords_index = extract_keywords_from_requirements(requirements_dir)

    # Save the requirements keywords index to a JSON file
    with open("keywords_req.json", "w", encoding="utf-8") as f:
        json.dump(requirements_keywords_index, f, indent=4)

    print("Requirement keywords extraction complete. File saved as keywords_req.json.")
