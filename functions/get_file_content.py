import config
import os
from google.genai import types

def get_file_content(working_directory, file_path):
    working_full_path = os.path.abspath(working_directory)

    if os.path.isabs(file_path):
        target_full_path = os.path.abspath(file_path)
    else:    
        target_full_path = os.path.abspath(os.path.join(working_directory, file_path))
    

    if not (target_full_path.startswith(working_full_path + os.sep)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

    if not os.path.isfile(target_full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'

    
    try:
        with open(target_full_path, "r") as f:
            file_content_string = f.read(config.MAX_CHARS)
            if len(f.read(1)):
                return file_content_string + f"[...File '{file_path}' truncated at {config.MAX_CHARS} characters]"
            else:
                return file_content_string
    except Exception as e:
        return f"Error: {e}"


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Gets contents of a file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory.",
            ),
        },
    ),
)