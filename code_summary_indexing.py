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

def load_json(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_keywords(text):
    """Extract keywords from the given text, removing stop words."""
    if text:  # Check if text is not None or empty
        return list(set(word for word in text.split() if word.lower() not in stop_words))
    return []  # Return an empty list if text is None or empty

# Load parsed data and code summaries
parsed_data = load_json("parsed_info.json")
code_summaries = load_json("code_summaries.json")

# Initialize the keywords dictionary
keywords_index = {}

# Process each class in parsed data
for class_data in parsed_data:
    class_name = class_data['class_name']
    docstring = class_data.get('docstring', '')  # Ensure default to empty string if None
    
    # Extract keywords from the parsed docstring
    keywords = extract_keywords(docstring)

    # Include method names, parameters, and attributes in keywords
    methods = class_data.get('methods', [])
    attributes = class_data.get('attributes', [])
    
    # Extract keywords from methods and attributes
    for method in methods:
        keywords.append(method['method_name'])
        keywords.extend(extract_keywords(' '.join(method.get('parameters', []))))  # Include parameters
    
    keywords.extend(attributes)  # Include attributes
    keywords_index[class_name] = list(set(keywords))  # Remove duplicates

# Process each class in the code summaries
for class_name, summary in code_summaries.items():
    print(f"Extracting keywords for code summary of class: {class_name}")  # Print current class

    # Extract keywords from the code summary
    summary_keywords = extract_keywords(summary)

    # Combine keywords from parsed info and code summary
    if class_name in keywords_index:
        keywords_index[class_name].extend(summary_keywords)
        keywords_index[class_name] = list(set(keywords_index[class_name]))  # Remove duplicates
    else:
        keywords_index[class_name] = summary_keywords

# Save keywords index to a JSON file
with open("keywords.json", "w", encoding="utf-8") as f:
    json.dump(keywords_index, f, indent=4)

print("Keyword extraction complete. File saved as keywords.json.")
