import json
from collections import defaultdict

def load_json(file_path):
    """Load data from JSON file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def map_top_classes_to_requirements(requirements_keywords, classes_keywords, top_n=3):
    """Map requirements to top N classes based on keyword matching."""
    mapping = {}

    # Compare each requirement with class keywords
    for req_file, req_keywords in requirements_keywords.items():
        print(f"Mapping requirement: {req_file}")  # Print current requirement being processed
        class_count = {}

        for class_name, class_keywords in classes_keywords.items():
            # Count the number of matching keywords
            match_count = sum(1 for keyword in req_keywords if keyword in class_keywords)
            if match_count > 0:
                class_count[class_name] = match_count

        # Sort classes by match count and select top N
        top_classes = sorted(class_count.items(), key=lambda item: item[1], reverse=True)[:top_n]
        mapping[req_file] = {class_name: count for class_name, count in top_classes}

    return mapping

if __name__ == "__main__":
    # Load keywords from JSON files
    requirements_keywords = load_json("keywords_req.json")
    classes_keywords = load_json("keywords.json")

    # Perform mapping
    mapping_results = map_top_classes_to_requirements(requirements_keywords, classes_keywords, top_n=3)

    # Save mapping results to a JSON file
    with open("mapping3.json", "w", encoding="utf-8") as f:
        json.dump(mapping_results, f, indent=4)

    print("Mapping of requirements to top 3 classes complete. File saved as mapping3.json.")
