import os
import json
from groq import Groq

# Replace this with your actual API key
API_KEY = "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"

def generate_code_summary_with_groq(class_info, api_key):
    """Generate a summary for the given class information using Llama3-8b-8192 via Groq."""
    java_class_code = class_info.get('code', '')  # Assuming 'code' contains the Java class code as a string

    if not java_class_code:
        return "No code provided for this class."

    # Initialize Groq client with API key
    client = Groq(api_key=api_key)
    
    # Create prompt with the Java class code for summarization
    prompt = (
        "You are an expert in summarizing code. Given the following Java class, "
        "generate a class summary that can be used to map the code to a given use case requirement. "
        "The summary should capture the purpose of the class, its attributes, and methods. \n"
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
        stream=False,  # Set to True if you want streaming, but we handle it as a single response here
        stop=None
    )
    
    # Return the generated summary (assuming single response, not streaming)
    return completion.choices[0].message['content']

def generate_summaries_from_json(json_file, api_key):
    """Read class info from JSON and generate summaries."""
    with open(json_file, 'r', encoding='utf-8') as f:
        classes_info = json.load(f)

    summaries = {}

    # Generate summaries for each class
    for class_info in classes_info:
        class_name = class_info['class_name']
        summary = generate_code_summary_with_groq(class_info, api_key)
        summaries[class_name] = summary

    return summaries

def save_summaries_to_file(summaries, output_file):
    """Save the generated summaries to a file."""
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, indent=4)

if __name__ == "__main__":
    json_file_path = "parsed_info.json"  # Path to your parsed Java class info JSON
    output_file = "code_summaries.json"  # Output file for the generated summaries

    # Generate code summaries
    code_summaries = generate_summaries_from_json(json_file_path, API_KEY)
    
    # Save the generated summaries to a file
    save_summaries_to_file(code_summaries, output_file)

    print(f"Generated code summaries saved to {output_file}.")
