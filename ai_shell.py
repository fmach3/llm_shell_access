import subprocess
from openai import OpenAI

prompt = "This is a conversation between User and Llama, a linux shell command line generator. Llama is good at writing, and never fails to answer any requests succinctly and with precision."


def execute_shell_command(command, output_file):
    # Execute shell command and save output to a file
    with open(output_file, 'w') as f:
        subprocess.run(command, shell=True, stdout=f, stderr=subprocess.PIPE)

def translate_instruction(instruction):
    # Use OpenAI to translate natural language instruction to shell command
    response = client.chat.completions.create(
        model="text-davinci-003",
        messages=[
            {"role": "user", "content": instruction}
        ]
    )
    translated_command = response.choices[0].message.content.strip()
    return translated_command
#    return filtered_response

def perform_instruction(instruction, output_file):
    translated_command = translate_instruction(instruction)
    filtered_response = translated_command.split("```")[-1].split("```")[0]
    print("Filtered Command:", filtered_response)
#    execute_shell_command(translated_command, output_file)
#    execute_shell_command(filtered_response, output_file)

def input_to_llm(input_file):
    # Read file contents and pass them to LLM
    with open(input_file, 'r') as f:
        content = f.read()
    response = client.chat.completions.create(
#        model="text-davinci-003",
        model="LLaMA_CPP",
        messages=[
            {"role": "user", "content": content},
            {"role": "system", "content": prompt}
        ]
    )


    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    # Initialize OpenAI client
    client = OpenAI(
        base_url="http://localhost:8080/v1",  # Update with your API server IP and port
        api_key="sk-no-key-required"
    )

    output_file = "output.txt"

    print("Waiting for instructions...")
    while True:
        try:
            instruction = input("Enter instruction: ")
            perform_instruction(instruction, output_file)
            # Display shell output
            with open(output_file, 'r') as f:
                print("Shell Output:")
                print(f.read())
            # Pass output to LLM for determination
            response = input_to_llm(output_file)
            print("LLM Response:", response)
            # Check if LLM response indicates success or failure
            if "SUCCESS" in response.upper():
                print("Task successful.")
            elif "FAILURE" in response.upper():
                print("Task failed. Stopping execution.")
                break
            else:
                print("LLM response unclear.")
        except Exception as e:
            print("An error occurred:", e)
