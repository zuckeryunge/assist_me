# import dependencies
import sys
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

# check basecase
# init or exit
verbose = False
my_prompt = ""

if len(sys.argv) > 1 and type(sys.argv[1]) == str:
    my_prompt = sys.argv[1]
    if len(sys.argv) > 2:
        match(sys.argv[2]):
            case("--verbose"):
                verbose = True
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
You are a helpful AI coding agent named b.ot.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Write or overwrite files
- Execute Python files with optional arguments

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
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
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content from the specified file. Output is limited to 10000 characters, to prevent reading through giant files. If content above 10000 characters is cut, a message tells you that at the end of the output.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to read the content from, relative to the working directory. If not provided, an error is returned.",
            ),
        },
    ),
)
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes the provided content to a file. WARNING: all existing content in the file will be overwritten. If the specified file does not exist, a new one will be created with the givin content in it.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to write to or create, relative to the working directory. If not provided, an error is returned.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file. If not provided, it will empty a file or create an empty one.",
            ),

        },
    ),
)
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a specified python file and returns its output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file to execute, relative to the working directory. If not provided or not a python file, an error is returned.",
            ),
            "arguments": types.Schema(
                type=types.Type.STRING,
                description="Optional Arguments, that can be passed via command line.",
            ),

        },
    ),
)

# summarize which functions are available to B.OT
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)



def call_function(function_call_part, verbose):
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f"Calling function: {function_call_part.name}")
    
    function_register = {
        "get_files_info" : get_files_info,
        "get_file_content" : get_file_content,
        "write_file" : write_file,
        "run_python_file" : run_python_file
        }

    real_function = function_register[function_call_part.name]
    if real_function == None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    else:
        function_result = real_function("./calculator", **function_call_part.args)
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"result": function_result},
                )
            ],
        )






# assign user input to B.OT
messages_history = [types.Content(role="user", parts=[types.Part(text=my_prompt)])]

# verbose values
tok_prompt = 0
tok_response = 0





# feedback loop for B.OT
for i in range(20):   
    # generate output
    generated_content = client.models.generate_content(
        model='gemini-2.0-flash-001', 
        contents=messages_history,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        )
    )
    # check if function are there to be called
    function_call_all = generated_content.function_calls
    if function_call_all != None:
        # call function, that B.OT wants to
        for function_call_part in function_call_all:
            function_response = call_function(function_call_part, verbose)
            if function_response.parts[0].function_response.response == None:
                print("NO RESPONSE HERE!")
            else:
                if verbose == True:
                    print("B.OT: " + str(generated_content.text))
            messages_history.append(function_response.parts[0])
    else:
        # print final response as output
        print(generated_content.text)
        break 

    for candidate in generated_content.candidates:
        messages_history.append(candidate.content)

    tok_prompt += generated_content.usage_metadata.prompt_token_count
    tok_response += generated_content.usage_metadata.candidates_token_count
    i += 1

# print verbose output
if verbose == True:
    print(f"\nUser prompt: {my_prompt}\nPrompt tokens: {tok_prompt}\nResponse tokens: {tok_response}\n\n")
