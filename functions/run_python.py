import os
import subprocess

# function for safely executing things by aigent
def execute(path_to_exec_file):
    print(os.path.abspath(path_to_exec_file))
    outout = subprocess.run(path_to_exec_file, capture_output=True, timeout=30, check=True)
    print("one")
    print(outout)
    exec_out = f"STDOUT: {subprocess.CompletedProcess.stdout}"
    print(exec_out)
    print("two")
    exec_err = f"STDERR: {subprocess.CompletedProcess.stderr}"
    print(exec_err)
    print("three")

    return exec_out, exec_err


# exported function for use by aigent
# also handles input errors
def run_python_file(working_directory, file_path):
    try:
        if file_path.startswith("/") or file_path.startswith("../"):
            print("1")
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path
            print("2")

        if os.path.isdir(file_abspath) or file_path == None or file_path == "." or file_path == "":
            print("3")
            return f'Error: No path given or is a directory: "{file_path}"'
        else:
            if not os.path.exists(file_abspath):
                print("4")
                return f'Error: File "{file_path}" not found.' 
            elif not file_abspath.endswith(".py"):
                print("5")
                return f'Error: "{file_path}" is not a Python file.'
            else:
                print("6")
                execute(os.path.join(working_directory, file_path))
    except Exception as e:
        print("eee")
        print(f"Error: executing Python file: {e}")
