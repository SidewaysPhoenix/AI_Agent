import os
import time, re
import sys
import config
from google import genai
from google.genai import types
from dotenv import load_dotenv
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

#if no prompt exit
try:
    user_prompt = sys.argv[1]
except Exception:
    sys.exit(1)

#functions for LLM to use
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)

#activation
messages = [
    types.Content(
        role="user", 
        parts=[types.Part(text=user_prompt)]
    ),
]

def call_function(function_call_part, verbose=False):
            if verbose:
                print(f"Calling function: {function_call_part.name}({function_call_part.args})")
            else: 
                print(f" - Calling function: {function_call_part.name}")
            function_map = {
                "get_file_content": get_file_content,
                "get_files_info": get_files_info,
                "run_python_file": run_python_file,
                "write_file": write_file
            }
        

            if function_call_part.name not in function_map:
                return types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"error": f"Unknown function: {function_call_part.name}"},
                        )
                    ],
                )
            else:
                args = function_call_part.args
                args["working_directory"] = "./calculator"
                result = function_map[function_call_part.name](**args)
                return types.Content(
                    role="user",
                    parts=[
                        types.Part.from_function_response(
                            name=function_call_part.name,
                            response={"result": result},
                        )
                    ],
                )

any_tool_call = False



for i in range(20):
    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash-001', 
            contents=messages, 
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=config.SYSTEM_PROMPT
            )
        )
        
        prompt_token_count = response.usage_metadata.prompt_token_count
        response_token_count = response.usage_metadata.candidates_token_count
        verbose = "--verbose" in sys.argv
        if verbose:
            print(f"User prompt: {sys.argv[1]}")
            print(f"Prompt tokens: {prompt_token_count}")
            print(f"Response tokens: {response_token_count}")

        for responses in response.candidates:
            messages.append(responses.content)
            for part in responses.content.parts:
                if part.function_call is not None:
                    any_tool_call = True
                    result = call_function(part.function_call, verbose)
                    messages.append(result)

        if any_tool_call:
            time.sleep(0.25)
            continue

        if response.text:
            print(response.text)
            break

    except Exception as e:
        msg = str(e)
        # Handle Gemini 429: RESOURCE_EXHAUSTED – sleep & retry instead of exit(1)
        if "RESOURCE_EXHAUSTED" in msg or "quota" in msg.lower() or "429" in msg:
            # Try to read RetryInfo delay like "retryDelay': '42s'"
            m = re.search(r"retryDelay['\"]?:\s*'(\d+)s'", msg)
            delay = int(m.group(1)) if m else 10  # fallback seconds
            # Small jitter and cap
            delay = min(delay + 1, 45)
            if "--verbose" in sys.argv:
                print(f"Rate limited (429). Waiting {delay}s then retrying...")
            time.sleep(delay)
            continue  # try the next loop iteration
        print(f"Error: {e}")
        sys.exit(1)


