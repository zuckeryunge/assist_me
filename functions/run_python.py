import os
import subprocess

# function for safely executing things by aigent
def execute(path_to_exec_file):
    exec_done = subprocess.run(["python3", path_to_exec_file], capture_output=True, timeout=30, check=True)
    exec_out = f"STDOUT: {str(exec_done.stdout)}"
    exec_err = f"STDERR: {str(exec_done.stderr)}"

    return exec_out, exec_err


# exported function for use by aigent
# also handles input errors
def run_python_file(working_directory, file_path):
    try:
        message = "\n--------------- wrong ---------------"
        result = "No output produced."
        if file_path.startswith("/") or file_path.startswith("../"):
            result = f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path

            if os.path.isdir(file_abspath) or file_path == None or file_path == "." or file_path == "":
                result = f'Error: No path given or is a directory: "{file_path}"'
            else:
                if not os.path.exists(file_abspath):
                    result = f'Error: File "{file_path}" not found.' 
                elif not file_abspath.endswith(".py"):
                    result = f'Error: "{file_path}" is not a Python file.'
                else:
                    message = "\n--------------- executing ---------------"
                    result = execute(os.path.join(working_directory, file_path))
        print(message)
        return result
    except Exception as e:
        print(message)
        print(f"Error: executing Python file: {e}")
