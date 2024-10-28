import os
import json
import javalang
from groq import Groq

# Replace this with your actual API key
API_KEY = "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"

def parse_java_file(file_path):
    """Parse a Java file and extract the class code."""
    with open(file_path, 'r', encoding='utf-8') as file:
        code = file.read()

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

def generate_code_summary_with_groq(class_info, api_key):
    """Generate a summary for the given class information using Llama3-8b-8192 via Groq."""
    java_class_code = class_info.get('code', '')  # Extract Java class code

    if not java_class_code:
        return "No code provided for this class."

    # Initialize Groq client with API key
    client = Groq(api_key=api_key)

    # Create prompt with the Java class code for summarization
    prompt = (
        "You are an expert in summarizing code. Given the following Java class, "
        "generate a class summary that can be used to map the code to a given use case requirement. "
        "The summary should capture the purpose of the class, its attributes, and methods.\n"
        f"Here is the code:\n{java_class_code}"
    )

    # Call the Groq API to generate the summary
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": prompt
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,  # Handle as a single response here
        stop=None
    )

    # Correctly access the content of the first choice
    if hasattr(completion, 'choices') and len(completion.choices) > 0:
        return completion.choices[0].message.content or "No content returned"
    else:
        return "No choices returned"

def generate_summaries_for_directory(src_directory, api_key):
    """Parse all Java files in a directory and generate summaries."""
    # Parse the directory and get all class info
    classes_info = parse_directory(src_directory)
    
    summaries = {}

    # Generate summaries for each class
    for class_info in classes_info:
        class_name = class_info['class_name']
        summary = generate_code_summary_with_groq(class_info, api_key)
        
        # Print the summary for each class
        print(f"Class: {class_name}")
        print(f"Summary: {summary}\n")
        
        summaries[class_name] = summary

    return summaries

def save_summaries_to_file(summaries, output_file):
    """Save the generated summaries to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=4)

if __name__ == "__main__":
    src_directory = "./src"  # Path to your directory containing Java files
    output_file = "code_summaries.json"  # Output file for the generated summaries

    # Generate code summaries
    code_summaries = generate_summaries_for_directory(src_directory, API_KEY)
    
    # Save the generated summaries to a file
    save_summaries_to_file(code_summaries, output_file)

    print(f"Generated code summaries saved to {output_file}.")
