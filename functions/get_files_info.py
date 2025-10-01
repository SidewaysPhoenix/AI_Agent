import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    full_path = os.path.abspath(os.path.join(working_directory, directory))
    abs_working = os.path.abspath(working_directory)



    if not (full_path == abs_working or full_path.startswith(abs_working + os.sep)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    try:
        contents = os.listdir(full_path)
        breakdown = []
        for content in contents:
            fuller_path = os.path.join(full_path, content)
            breakdown.append(f"- {content}: file_size={os.path.getsize(fuller_path)} bytes, is_dir={os.path.isdir(fuller_path)}")
        return "\n".join(breakdown)
    except Exception as e:
        return f"Error: {e}"

    
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



