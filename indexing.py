import json
from transformers import BertTokenizer, BertModel
import torch
import re

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

def load_json(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def clean_text(text):
    """Clean and preprocess the text for keyword extraction."""
    # Remove non-alphanumeric characters and convert to lowercase
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text.lower())
    return text

def extract_significant_keywords(methods, attributes, parsed_docstring):
    """Extract significant keywords from methods, attributes, and docstrings."""
    keywords = set()

    # Define a list of stopwords to filter out
    stopwords = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your",
        "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she",
        "her", "hers", "herself", "it", "its", "itself", "they", "them", "their",
        "theirs", "themselves", "what", "which", "who", "whom", "this", "that",
        "these", "those", "am", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while", "of",
        "at", "by", "for", "with", "about", "against", "between", "into", "through",
        "during", "before", "after", "above", "below", "to", "from", "up", "down",
        "in", "out", "on", "off", "over", "under", "again", "further", "then",
        "once", "here", "there", "when", "where", "why", "how", "all", "any",
        "both", "each", "few", "more", "most", "other", "some", "such", "no", "nor",
        "not", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can",
        "will", "just", "don", "should", "now"
    ])

    # Add method names and parameters
    for method in methods:
        keywords.add(method['method_name'])
        keywords.update(method['parameters'])
    
    # Add attributes
    keywords.update(attributes)
    
    # Process parsed docstring
    if parsed_docstring:
        cleaned_docstring = clean_text(parsed_docstring)
        tokens = cleaned_docstring.split()  # Simple split by whitespace
        for token in tokens:
            if token and token not in stopwords:  # Avoid adding empty strings and stopwords
                keywords.add(token)

    return list(keywords)  # Convert back to list

# Load parsed data
parsed_data = load_json("parsed_info.json")

# Initialize the keyword list and vector list
keywords_index = {}
vector_index = {}

# Process each class in the parsed data
for class_data in parsed_data:
    class_name = class_data['class_name']
    methods = class_data.get('methods', [])
    attributes = class_data.get('attributes', [])
    parsed_docstring = class_data.get('docstring', '')

    # --- Keyword Indexing ---
    print(f"Processing class: {class_name}")  # Print current class
    
    # Extract relevant significant keywords
    keywords = extract_significant_keywords(methods, attributes, parsed_docstring)
    keywords_index[class_name] = keywords

# Save keywords index to JSON file
with open("keywords_index.json", "w", encoding="utf-8") as f:
    json.dump(keywords_index, f, indent=4)

# --- Vector Indexing for Keywords ---
for class_name, keywords in keywords_index.items():
    # Combine keywords into a single string
    text_combined = ' '.join(keywords)

    # Tokenize and generate BERT embeddings
    inputs = tokenizer(text_combined, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()  # Mean pooling for sentence embedding
    
    # Store embedding vector in the vector index
    vector_index[class_name] = embeddings

# Convert vector_index values to lists for JSON serialization
vector_index_normalized = {k: v.tolist() for k, v in vector_index.items()}

# Save vector index to JSON file
with open("vector_index.json", "w", encoding="utf-8") as f:
    json.dump(vector_index_normalized, f, indent=4)

print("Keyword indexing and vectorization complete. Files saved as keywords_index.json and vector_index.json.")
