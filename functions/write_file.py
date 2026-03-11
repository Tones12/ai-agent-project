import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    except Exception as e:
        return f'Error getting absolute directories: {e}'
    
    try:
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        valid_file = os.path.isdir(target_file)
    except Exception as e:
        return f'Error validating file location and/or file: {e}'
    
    if valid_target_file == False:
        return (f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
    if valid_file == True:
        return (f'Error: Cannot write to "{file_path}" as it is a directory')
    
    try:
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
    except Exception as e:
        return f'Error: make directories error: {e}'

    try:
        with open(target_file, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: write unsuccessful: {e}'
    
