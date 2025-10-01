import os
import sys
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not abs_file_path.startswith(abs_working):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_file_path[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        cp = subprocess.run([sys.executable, abs_file_path], timeout=30, stdout=subprocess.PIPE, stderr = subprocess.PIPE, cwd=abs_working, text=True)
        out = f"STDOUT: {cp.stdout}\nSTDERR: {cp.stderr}"
        if cp.stdout == "" and cp.stderr =="":
            return "No output produced."
        if cp.returncode != 0: 
            out += f"\nProcess exited with code {cp.returncode}"
        return out
    except Exception as e:
        return f"Error: executing Python file: {e}"



schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs python file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="file path to file and the arguments for the file.",
            ),
        },
    ),
)