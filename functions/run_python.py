import os

# function for safely executing things by aigent
def execute():
    # do the things that have to be done
    return 








# exported function for use by aigent
# also handles input errors
def run_python_file(working_directory, file_path):
    try:
        if file_path.startswith("/") or file_path.startswith("../"):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path

        if os.path.isdir(file_abspath) or file_path == None or file_path == "." or file_path == "":
            return f'Error: No path given or is a directory: "{file_path}"'
        else:
            if not os.path.exists(file_abspath):
                return f'Error: File "{file_path}" not found.' 
            elif not file_abspath.endswith(".py"):
                return f'Error: "{file_path}" is not a Python file.'
            else:
                return execute()
    except Exception as e:
        print(f"Error: executing Python file: {e}")
