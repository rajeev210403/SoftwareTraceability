import os
import json
import javalang

def parse_java_file(file_path):
    """Parse a Java file and extract classes, methods, attributes, and comments."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

    # Parse the Java code
    tree = javalang.parse.parse(code)
    
    classes_info = []

    # Iterate through the parsed tree to find class and method declarations
    for node in tree.types:
        class_info = {
            'class_name': node.name,
            'methods': [],
            'attributes': [],
            'docstring': []
        }

        # Extract class-level docstring (if any)
        if hasattr(node, 'documentation') and node.documentation is not None:
            class_info['docstring'].extend(node.documentation)

        # Extract class attributes and methods
        for member in node.body:
            if isinstance(member, javalang.tree.FieldDeclaration):
                for variable in member.declarators:
                    class_info['attributes'].append(variable.name)  # Use variable.name instead of variable.variable
            elif isinstance(member, javalang.tree.MethodDeclaration):
                method_info = {
                    'method_name': member.name,
                    'parameters': [param.name for param in member.parameters],
                    'docstring': member.documentation if hasattr(member, 'documentation') and member.documentation is not None else []
                }
                class_info['methods'].append(method_info)

        classes_info.append(class_info)

    return classes_info

def parse_directory(src_directory):
    """Parse all Java files in the specified directory."""
    all_classes_info = []

    for root, _, files in os.walk(src_directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                class_info = parse_java_file(file_path)
                all_classes_info.extend(class_info)

    return all_classes_info

def save_to_json(data, json_file):
    """Save the parsed data to a JSON file."""
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    src_directory = "./src"  # Path to the directory containing Java files
    json_file_path = "parsed_info.json"  # Path to save the JSON file

    parsed_info = parse_directory(src_directory)
    
    # Save the parsed information to a JSON file
    save_to_json(parsed_info, json_file_path)

    print(f"Parsed information saved to {json_file_path}.")
