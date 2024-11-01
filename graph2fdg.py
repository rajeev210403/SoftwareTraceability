import networkx as nx
import matplotlib.pyplot as plt

# Load the FDG from the GEXF file
fdg = nx.read_gexf('./itrust_fdg.gexf')

# Customize the layout and style for better visualization
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(fdg, k=0.15)  # Set layout (spring layout looks nice for dependency graphs)

# Draw nodes and edges with specific styles
nx.draw_networkx_nodes(fdg, pos, node_size=50, node_color='skyblue', alpha=0.7)
nx.draw_networkx_edges(fdg, pos, edge_color='gray', alpha=0.5)
nx.draw_networkx_labels(fdg, pos, font_size=6, font_color="black", font_family="sans-serif")

plt.title("Function Dependency Graph (FDG) of iTrust")
plt.show()
