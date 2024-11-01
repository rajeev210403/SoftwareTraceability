import os
import json
import re
import javalang

def extract_docstrings(code):
    """Extracts Java-style docstrings (multi-line comments) from the given code."""
    pattern = r'/\*\*(.*?)\*/'  # Regex pattern to match Java docstring comments
    matches = re.findall(pattern, code, re.DOTALL)
    return [match.strip().replace("\n", " ").replace("*", "").strip() for match in matches]

def parse_java_file(file_path):
    """Parse a Java file and extract classes, methods, attributes, and comments."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                code = file.read()
            break
        except UnicodeDecodeError:
            print(f"Could not read file {file_path} with encoding {encoding}. Trying next encoding.")
            code = None
        except Exception as e:
            print(f"An unexpected error occurred while reading {file_path}: {e}")
            code = None

    if code is None:
        print(f"Skipping file {file_path} due to encoding issues.")
        return None

    try:
        tree = javalang.parse.parse(code)
    except javalang.parser.JavaSyntaxError:
        print(f"Syntax error in file {file_path}")
        return None
    
    classes_info = []
    docstrings = extract_docstrings(code)

    # Store the current docstring index to match method docstrings
    docstring_index = 0

    # Iterate through the parsed tree to find class and method declarations
    for node in tree.types:
        class_info = {
            'class_name': node.name,
            'methods': [],
            'attributes': [],
            'docstring': docstrings[docstring_index] if docstring_index < len(docstrings) else None
        }
        docstring_index += 1  # Move to the next docstring after assigning

        for member in node.body:
            if isinstance(member, javalang.tree.FieldDeclaration):
                for variable in member.declarators:
                    class_info['attributes'].append(variable.name)
            elif isinstance(member, javalang.tree.MethodDeclaration):
                method_info = {
                    'method_name': member.name,
                    'parameters': [param.name for param in member.parameters],
                    'docstring': None  # Initialize method docstring
                }

                # Check for a docstring right before the method declaration
                if docstring_index < len(docstrings):
                    method_info['docstring'] = docstrings[docstring_index]
                    docstring_index += 1  # Move to the next docstring after assigning
                
                class_info['methods'].append(method_info)

        classes_info.append(class_info)

    print(f"Processed file successfully: {file_path}")
    
    return classes_info

def parse_directory(src_directory):
    """Parse all Java files in the specified directory."""
    all_classes_info = []

    for root, _, files in os.walk(src_directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                class_info = parse_java_file(file_path)
                if class_info:  # Ensure class_info is not None
                    all_classes_info.extend(class_info)

    return all_classes_info

def save_to_json(data, json_file):
    """Save the parsed data to a JSON file."""
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    src_directory = "./datasets/iTrust"  # Path to the directory containing Java files
    json_file_path = "parsed_info.json"  # Path to save the JSON file

    parsed_info = parse_directory(src_directory)
    
    # Save the parsed information to a JSON file
    save_to_json(parsed_info, json_file_path)

    print(f"Parsed information saved to {json_file_path}.")
