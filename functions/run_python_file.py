import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python file with the given arguments and returns the output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to the Python file, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to be included in the run command"
                ),
            )
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    except Exception as e:
        return f'Error getting absolute directories: {e}'
    
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        valid_file = os.path.isfile(target_file)
    except Exception as e:
        return f'Error validating file location and/or file: {e}'
    
    if valid_target_file == False:
        return (f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if valid_file == False:
        return (f'Error: "{file_path}" does not exist or is not a regular file')
    if not file_path.endswith('.py'):
        return (f'Error: "{file_path}" is not a Python file')
    
    try:
        command = ["python", target_file]
        if not args == None:
            command.extend(args)
    except Exception as e:
        return f"Error: setting up command arguments: {e}"
    try:
        command_output = subprocess.run(command, cwd=working_dir_abs, timeout=30, capture_output=True, text=True)
        output_string = ''
        if not command_output.returncode == 0:
            output_string += (f"Process exited with code {command_output.returncode}")
        if not command_output.stdout and not command_output.stderr:
            output_string += (f"No output produced")
        else:
            output_string += (f"STDOUT: {command_output.stdout}\nSTDERR: {command_output.stderr}")
    except Exception as e:
        return f'Error: executing Python file: {e}'

    return output_string


