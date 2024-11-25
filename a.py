import json
import networkx as nx

# Load the JSON file
def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Save updated JSON
def save_json(data, file_path):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Load the GEXF graph
def load_gexf(file_path):
    return nx.read_gexf(file_path)

# Get related classes (neighbors) from the graph
def get_related_classes(graph, class_list):
    related_classes = set()
    for cls in class_list:
        if cls in graph:
            # Add neighbors of the current class
            neighbors = graph.neighbors(cls)
            related_classes.update(neighbors)
    return list(related_classes)

# Process each requirement and augment classes
def augment_requirements_with_related_classes(json_file, gexf_file, output_file):
    # Load JSON and graph
    requirements_data = load_json(json_file)
    knowledge_graph = load_gexf(gexf_file)
    
    # Process each requirement
    for req, classes in requirements_data.items():
        # Get related classes from the graph
        related_classes = get_related_classes(knowledge_graph, classes)
        # Add related classes to the current list (avoid duplicates)
        requirements_data[req].extend(cls for cls in related_classes if cls not in classes)
    
    # Save the updated JSON
    save_json(requirements_data, output_file)
    print(f"Updated JSON saved to {output_file}")

json_file = "./llama_responses.json"   # Path to your JSON file
geft_file = "./itrust_fdg.gexf"       # Path to your .geft graph file
output_file = "augmented_requirements.json"  # Path to save updated JSON

augment_requirements_with_related_classes(json_file, geft_file, output_file)


