import os
from google.genai import types

def write_file(working_directory, file_path, content):

    working_full_path = os.path.abspath(working_directory)

    if os.path.isabs(file_path):
        target_full_path = os.path.abspath(file_path)
    else:    
        target_full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if os.path.commonpath([working_full_path, target_full_path]) != working_full_path:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'


    try:
        new_file_path = os.path.dirname(target_full_path)
        os.makedirs(new_file_path, exist_ok=True)
        with open(target_full_path, "w") as f:
            f.write(content)
    except Exception as e:
        return (f"Error: {e}")

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write"
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory",
            )
        },
    ),
)