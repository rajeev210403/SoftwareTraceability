import json
import networkx as nx
import matplotlib.pyplot as plt

# Load traceability links from the JSON file
def load_traceability_links(traceability_file):
    with open(traceability_file, 'r') as f:
        traceability_links = json.load(f)
    return traceability_links

# Load FDG from your existing .gexf file (assuming FDG is saved in GEXF format)
def load_fdg(fdg_file):
    fdg = nx.read_gexf(fdg_file)
    return fdg

# Create a combined graph of FDG and traceability links
def create_combined_graph(fdg, traceability_links):
    combined_graph = nx.Graph()
    combined_graph.add_nodes_from(fdg.nodes(data=True))  # Add FDG nodes with attributes
    combined_graph.add_edges_from(fdg.edges(data=True))  # Add FDG edges with attributes

    # Add traceability links as additional nodes and edges
    for requirement, related_classes in traceability_links.items():
        # Add a node for the requirement
        combined_graph.add_node(requirement, type='requirement', label=requirement)

        # Create edges between the requirement and relevant classes
        for class_name in related_classes:
            if class_name in fdg.nodes:  # Ensure the class exists in the FDG
                combined_graph.add_edge(requirement, class_name, type='traceability')

    return combined_graph

# Visualize the combined graph
def visualize_combined_graph(combined_graph):
    pos = nx.spring_layout(combined_graph)  # Position nodes using spring layout
    plt.figure(figsize=(12, 12))

    # Draw nodes with different colors for classes and requirements
    node_colors = [
        'skyblue' if combined_graph.nodes[node].get('type') == 'requirement' else 'lightgreen'
        for node in combined_graph.nodes
    ]

    nx.draw_networkx_nodes(combined_graph, pos, node_color=node_colors, node_size=500, alpha=0.7)
    nx.draw_networkx_labels(combined_graph, pos, font_size=10, font_family="sans-serif")
    
    # Draw edges with different colors for FDG dependencies and traceability links
    fdg_edges = [(u, v) for u, v, d in combined_graph.edges(data=True) if d.get('type') != 'traceability']
    traceability_edges = [(u, v) for u, v, d in combined_graph.edges(data=True) if d.get('type') == 'traceability']

    nx.draw_networkx_edges(combined_graph, pos, edgelist=fdg_edges, edge_color="gray", style="solid")
    nx.draw_networkx_edges(combined_graph, pos, edgelist=traceability_edges, edge_color="orange", style="dashed")

    plt.title("Combined Function Dependency and Traceability Graph")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    traceability_file = "traceability_links.json"  # Traceability links file from the previous step
    fdg_file = "fdg.gexf"  # GEXF file of the FDG for your Java files

    # Load traceability links and FDG
    traceability_links = load_traceability_links(traceability_file)
    fdg = load_fdg(fdg_file)

    # Create and visualize the combined graph
    combined_graph = create_combined_graph(fdg, traceability_links)
    visualize_combined_graph(combined_graph)
