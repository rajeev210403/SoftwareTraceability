import os
import networkx as nx
from pathlib import Path

# Specify the directory containing your requirement files
requirements_folder = Path('./datasets/iTrust/req/')

# Initialize Knowledge Graph (KG) and Function Dependency Graph (FDG)
KG = nx.Graph()
FDG = nx.DiGraph()

# Helper function to extract entities and dependencies (stubbed for simplicity)
def extract_entities_and_dependencies(text):
    # Placeholder function for entity extraction
    entities = set()
    dependencies = []
    
    # Process lines with simple "depends on" phrases
    for line in text.splitlines():
        if "depends on" in line:
            parts = line.split("depends on")
            if len(parts) == 2:
                requirement = parts[0].strip()
                function = parts[1].strip()
                entities.add(requirement)
                entities.add(function)
                dependencies.append((requirement, function))
    return entities, dependencies

# Process each requirement file
for req_file in requirements_folder.glob("UC*.txt"):
    with open(req_file, 'r') as file:
        content = file.read()
        
        # Extract entities and dependencies for the current file
        entities, dependencies = extract_entities_and_dependencies(content)
        
        # Add entities to the KG
        for entity in entities:
            KG.add_node(entity, type="entity")
        
        # Add dependencies to both KG and FDG
        for requirement, function in dependencies:
            KG.add_edge(requirement, function, relation="depends_on")
            FDG.add_node(requirement, type="requirement")
            FDG.add_node(function, type="function")
            FDG.add_edge(requirement, function, relation="depends_on")

# Export combined Knowledge Graph (KG) and Function Dependency Graph (FDG) as GEXF files
nx.write_gexf(KG, "combined_requirement_kg.gexf")
nx.write_gexf(FDG, "combined_requirement_fdg.gexf")

print("Combined Knowledge Graph and Function Dependency Graph generated and saved as GEXF files.")

#code for adding 2 numbers 
#code for adding 2 numbers

