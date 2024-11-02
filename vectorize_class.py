import json
from transformers import BertTokenizer, BertModel
import torch

# Load BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Define a set of common stop words
STOP_WORDS = set([
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
    "both", "each", "few", "more", "most", "other", "some", "such", "no", 
    "nor", "not", "only", "own", "same", "so", "than", "too", "very", "s", 
    "t", "can", "will", "just", "don", "should", "now"
])

def remove_unnecessary_words(text):
    """Remove unnecessary words from the text, handling None values."""
    if text is None:
        text = ''  # Treat None as an empty string
    # Split the text into words, remove stop words, and join them back
    return ' '.join(word for word in text.split() if word.lower() not in STOP_WORDS)

def load_json(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Load parsed data and code summaries
parsed_data = load_json("parsed_info.json")
code_summary = load_json("code_summaries.json")

# Initialize the vector index dictionary
vector_index = {}

# Process each class in the parsed data
for class_data in parsed_data:
    class_name = class_data['class_name']
    parsed_docstring = class_data.get('docstring', '')

    # Retrieve the code summary for the current class
    class_summary = code_summary.get(class_name, "")

    # --- Word Filtering ---
    # Remove unnecessary words from parsed docstring and class summary
    cleaned_docstring = remove_unnecessary_words(parsed_docstring)
    cleaned_summary = remove_unnecessary_words(class_summary)

    # Combine cleaned docstring and code summary into a single text block
    text_combined = f"{cleaned_docstring} {cleaned_summary}"

    print(f"Processing class: {class_name}")  # Print the current class name

    # Tokenize and generate BERT embeddings
    inputs = tokenizer(text_combined, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    
    # Mean pooling for sentence embedding
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().detach().numpy()
    
    # Store embedding vector in the vector index
    vector_index[class_name] = embeddings.tolist()  # Convert to list for JSON compatibility

# Save the vector index to a JSON file
with open("class_vector_index.json", "w", encoding="utf-8") as f:
    json.dump(vector_index, f, indent=4)

print("Vector indexing complete. File saved as class_vector_index.json.")
