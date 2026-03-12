import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
                ),
            },
        ),
    )

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    except Exception as e:
        return f'Error getting absolute directories: {e}'
    
    try:
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        valid_directory = os.path.isdir(target_dir)
    except Exception as e:
        return f'Error validating directories: {e}'
    
    if valid_target_dir == False:
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if valid_directory == False:
        return (f'Error: "{directory}" is not a directory')
    
    files = os.listdir(target_dir)

    file_string_list = []
    file_string = ''
    for file in files:
        file_size = os.path.getsize(f'{target_dir}/{file}')
        is_dir = os.path.isdir(f'{target_dir}/{file}')
        file_string_list.append(f'- {file}: file_size={file_size} bytes, is_dir={is_dir}\n')
    
    file_string = file_string.join(file_string_list)

    return file_string