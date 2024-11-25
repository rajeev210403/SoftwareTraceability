import os
import json
import javalang
from groq import Groq

# Replace this with your actual API key
API_KEY = "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"

def parse_java_file(file_path):
    """Parse a Java file and extract the class code."""
    encodings = ['utf-8', 'ISO-8859-1', 'windows-1252']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                code = file.read()
            break  # Exit the loop if successful
        except UnicodeDecodeError:
            print(f"Could not read file {file_path} with encoding {encoding}. Trying next encoding.")
            code = None
        except Exception as e:
            print(f"An unexpected error occurred while reading {file_path}: {e}")
            code = None

    if code is None:
        print(f"Skipping file {file_path} due to encoding issues.")
        return None

    # Parse the Java code using javalang
    try:
        tree = javalang.parse.parse(code)
    except javalang.parser.JavaSyntaxError:
        print(f"Syntax error in file {file_path}")
        return None
    
    class_code = []
    class_name = None

    # Iterate through the parsed tree to find class and method declarations
    for path, node in tree:
        if isinstance(node, javalang.tree.ClassDeclaration):
            class_name = node.name
            class_code.append(code)  # Append the entire class code (or customize to specific parts)
            break

    if class_name and class_code:
        return {"class_name": class_name, "code": '\n'.join(class_code)}
    else:
        return None

def parse_directory(src_directory):
    """Parse all Java files in the specified directory."""
    all_classes_info = []

    for root, _, files in os.walk(src_directory):
        for file in files:
            if file.endswith('.java'):
                file_path = os.path.join(root, file)
                class_info = parse_java_file(file_path)
                if class_info:
                    all_classes_info.append(class_info)

    return all_classes_info

def generate_class_traceability(classes_info, requirement, api_key):
    """Generate a list of classes related to a specific requirement using Groq."""
    # Join all class names and summaries for context
    classes_summary = "\n".join(f"Class {cls['class_name']}: {cls['code']}" for cls in classes_info)

    # Initialize Groq client with API key
    client = Groq(api_key=api_key)

    # Create prompt with the requirement and class summaries for traceability
    prompt = (
        "You are an expert in code traceability. Given the following classes and a specific requirement, "
        "list the names of classes that are relevant to the requirement. Provide the answer in JSON list format.\n"
        f"Requirement: {requirement}\n"
        f"Classes:\n{classes_summary}"
    )

    # Call the Groq API to generate the list of relevant classes
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "system", "content": prompt}],
        temperature=1,
        max_tokens=512,
        top_p=1,
        stream=False,
        stop=None
    )

    # Access the content of the first choice
    if hasattr(completion, 'choices') and len(completion.choices) > 0:
        return completion.choices[0].message.content or "No content returned"
    else:
        return "No choices returned"

def generate_traceability_links(requirements_file, src_directory, api_key):
    """Generate traceability links between requirements and classes."""
    # Parse the directory and get all class info
    classes_info = parse_directory(src_directory)
    
    traceability_links = {}

    # Read requirements from file
    with open(requirements_file, 'r', encoding='utf-8') as file:
        requirements = file.readlines()

    # Generate traceability links for each requirement
    for requirement in requirements:
        requirement = requirement.strip()
        relevant_classes = generate_class_traceability(classes_info, requirement, api_key)
        
        # Store traceability results
        traceability_links[requirement] = relevant_classes

    return traceability_links

def save_traceability_links_to_file(traceability_links, output_file):
    """Save the generated traceability links to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(traceability_links, f, indent=4)

if __name__ == "__main__":
    requirements_file = "./datasets/iTrust/req/UC1E1.txt"  # File containing requirements (one per line)
    src_directory = "./datasets/iTrust"    # Path to your directory containing Java files
    output_file = "1_test.json"  # Output file for the traceability links

    # Generate traceability links
    traceability_links = generate_traceability_links(requirements_file, src_directory, API_KEY)
    
    # Save the generated traceability links to a file
    save_traceability_links_to_file(traceability_links, output_file)

    print(f"Generated traceability links saved to {output_file}.")
