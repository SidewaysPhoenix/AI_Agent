import os
import sys
from google.genai import types
from dotenv import load_dotenv





load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai
client = genai.Client(api_key=api_key)

try:
    user_prompt = sys.argv[1]
except Exception:
    sys.exit(1)

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)

prompt_token_count = response.usage_metadata.prompt_token_count
response_token_count = response.usage_metadata.candidates_token_count
verbose = "--verbose" in sys.argv
if verbose:
    print(f"User prompt: {sys.argv[1]}")
    print(f"Prompt tokens: {prompt_token_count}")
    print(f"Response tokens: {response_token_count}")
    
print(response.text)