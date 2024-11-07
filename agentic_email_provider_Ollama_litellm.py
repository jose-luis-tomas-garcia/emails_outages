import os
import glob
import pdb
from litellm import completion
os.environ['SSL_CERT_FILE'] = '/usr/local/share/ca-certificates/ZscalerRootCA.crt'


def main():

    folder_to_analyze = 'emails_to_analyze/*'  # Adjust the pattern as needed
    analysis_instructions_file = 'instructions_for_extraction/instructions'

    for filepath in glob.glob(folder_to_analyze):
        with open(filepath, 'r') as file:
            email_content = file.read()
            analysis_instructions = open(analysis_instructions_file, 'r').read()

    prompt_input=f"""

    Consider the following email:

    -----------------------
    {email_content}

    -----------------------

    Now, please follow the following instructions:

    -----------------------

    {analysis_instructions}

    -----------------------

    """
    print(prompt_input)
    print('\n\n\nAwaiting LLM reply ...\n\n')
    response = completion(
    model="ollama/llama3.2",
    messages=[{ "content": prompt_input, "role": "user"}],
    api_base="http://192.168.0.73:11434"
    )
    
    print("LLM Response:")
    print(response['choices'][0]['message']['content'])

if __name__ == "__main__":
    main()