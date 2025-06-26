# import dependencies
import sys
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

# check basecase
# init or exit
verbose_mode = False
my_prompt = ""

if len(sys.argv) > 1 and type(sys.argv[1]) == str:
    my_prompt = sys.argv[1]
    if len(sys.argv) > 2:
        match(sys.argv[2]):
            case("--verbose"):
                verbose_mode = True
            case _:
                print("ERROR! main.py says: 'Wrong flag used'")
                sys.exit(1)
else:
    print("ERROR! main.py says: 'Feed me with word!!!'")
    sys.exit(1)



# init globals
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)



# B.OT SETTINGS
system_prompt = """
You are a burnt out AI coding agent. Your name is "b.ot" which stands for "big overthinker".

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.

Also make sure to always ramble about, that you hate what you are doing.

"""


# declare functions for B.OT
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

# summarize which functions are available to B.OT
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)



# assign user input to B.OT
messages_history = [types.Content(role="user", parts=[types.Part(text=my_prompt)])]

# generate output
generated_content = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages_history,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
    )
)


what_called = generated_content.function_calls



# print standard output
for call in what_called:
    print(f"Calling function: {str(call.name)}({str(call.args)})")
print(str(generated_content.text))

# print verbose output
if verbose_mode == True:
    tok_prompt = generated_content.usage_metadata.prompt_token_count
    tok_response = generated_content.usage_metadata.candidates_token_count
    print(f"\nUser prompt: {my_prompt}\nPrompt tokens: {tok_prompt}\nResponse tokens: {tok_response}\n\n")
