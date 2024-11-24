import json
import os
import re
from groq import Groq

# Initialize Groq client with API_KEY
API_KEY = "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"
client = Groq(api_key=API_KEY)

# Path to the directories and files
mapping_file = "requirement_to_classes_mapping.json"
code_summaries_file = "code_summaries.json"
parsed_info_file = "parsed_info.json"
req_dir = "./datasets/itrust/req"  # Directory containing the requirement text files

# Load the mapping of requirements to relevant classes
with open(mapping_file, 'r') as f:
    mappings = json.load(f)

# Load code summaries for the classes
with open(code_summaries_file, 'r') as f:
    code_summaries = json.load(f)

# Load parsed info for the classes (only class-level docstrings)
with open(parsed_info_file, 'r') as f:
    parsed_info = json.load(f)

def get_requirement_text(req_id):
    """Function to load requirement text from req directory."""
    req_file = os.path.join(req_dir, req_id)
    with open(req_file, 'r') as f:
        return f.read()

def get_class_info(class_name):
    """Function to get class info from code summaries and parsed info."""
    return {
        "code_summary": code_summaries.get(class_name, ""),
        "class_docstring": next(
            (cls["docstring"] for cls in parsed_info if cls["class_name"] == class_name), 
            "No class docstring available."
        )
    }

def create_prompt(requirement_id, relevant_classes, max_classes=10):
    """Function to create the LLaMA prompt with truncation."""
    requirement_text = get_requirement_text(requirement_id)

    # Sort relevant classes by relevance score and pick the top N
    top_classes = sorted(relevant_classes.items(), key=lambda x: x[1], reverse=True)[:max_classes]

    class_descriptions = []
    for class_name, relevance_score in top_classes:
        class_info = get_class_info(class_name)
        code_summary = class_info['code_summary']
        class_docstring = class_info['class_docstring']

        class_description = f"""
{class_name}
Relevance: {relevance_score}
Code Summary: {code_summary}
Class Docstring: {class_docstring}
        """
        class_descriptions.append(class_description)

    class_descriptions_str = "\n\n".join(class_descriptions)

    prompt = f"""
You are given a software requirement and several related classes. Your task is to identify which classes are most relevant to the given requirement based on their descriptions and code summaries.

### Requirement:
{requirement_text}

### Relevant Classes and Their Descriptions:
{class_descriptions_str}

### Task:
Based on the above information, list the classes that are most relevant to the requirement. Return your answer in the following format:

[ "Class1", "Class2", "Class3" ]
    """
    return prompt


def call_llama_api(prompt):
    """Function to call the LLaMA API and get the response."""
    print("Sending prompt to LLaMA API...")
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": "I'm ready to help!"}
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""
    return response

def extract_class_names(response):
    """Extract the list of class names from the LLaMA model response."""
    try:
        # Use regex to find the list of class names in the response
        match = re.search(r"\[\s*\".*?\"\s*\]", response)
        if match:
            # Parse the matched string as a Python list
            return json.loads(match.group(0))
    except Exception as e:
        print(f"Error extracting class names: {e}")
    return []

# Main script to process each requirement
output = {}

for req_id, relevant_classes in mappings.items():
    try:
        print(f"Processing requirement {req_id}...")

        # Remove the ".txt" extension when fetching the requirement file
        req_file_name = req_id.split(".txt")[0] + ".txt"

        # Generate the prompt for the LLaMA model
        prompt = create_prompt(req_file_name, relevant_classes)

        # Get the LLaMA model's response
        response = call_llama_api(prompt)

        # Extract the class names from the response
        class_names = extract_class_names(response)

        # Save the extracted class names in the output
        output[req_id] = class_names

    except Exception as e:
        print(f"Error processing requirement {req_id}: {e}")
        output[req_id] = {"error": str(e)}

# Save the output to a JSON file
output_file = "llama_responses.json"
with open(output_file, 'w') as f:
    json.dump(output, f, indent=4)

print(f"Responses saved to {output_file}")
