# import dependencies
import sys
import os
from dotenv import load_dotenv

from google import genai
from google.genai import types


# get globals
load_dotenv()
api_key = os.environ.get('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
verbose_mode = False
my_prompt = ""


# init or exit
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


# assign input
messages_history = [types.Content(role="user", parts=[types.Part(text=my_prompt)])]


# generate output
generated_content = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages_history
)
tok_prompt = generated_content.usage_metadata.prompt_token_count
tok_response = generated_content.usage_metadata.candidates_token_count


# print standard output
print(generated_content.text)


# print verbose output
if verbose_mode == True:
    print(f"User prompt: {my_prompt}\nPrompt tokens: {tok_prompt}\nResponse tokens: {tok_response}")
