import os
import javalang
import networkx as nx

# Directory path to iTrust source files
source_dir = './datasets/iTrust/'  # Update this to the location of your Java source files

# Initialize a directed graph for the FDG
fdg = nx.DiGraph()

# Parse Java files and populate the FDG
def parse_java_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".java"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as java_file:
                    try:
                        tree = javalang.parse.parse(java_file.read())
                        analyze_java_file(tree, file)
                    except Exception as e:
                        print(f"Failed to parse {file}: {e}")

def analyze_java_file(tree, filename):
    # Loop through classes in the file
    for _, class_decl in tree.filter(javalang.tree.ClassDeclaration):
        class_name = class_decl.name
        fdg.add_node(class_name, type='class', filename=filename)
        
        # Analyze methods in the class
        for method in class_decl.methods:
            method_name = f"{class_name}.{method.name}"
            fdg.add_node(method_name, type='method')
            fdg.add_edge(class_name, method_name)  # Edge from class to its method
            
            # Look for method calls within each method
            for _, node in method.filter(javalang.tree.MethodInvocation):
                called_method = node.member
                fdg.add_edge(method_name, called_method)  # Edge from method to called method

# Generate FDG from Java files
parse_java_files(source_dir)

# Save the FDG to a file
nx.write_gexf(fdg, 'itrust_fdg.gexf')
print("FDG generated and saved as 'itrust_fdg.gexf'")
