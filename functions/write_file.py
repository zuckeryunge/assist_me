import os

def write_file(working_directory, file_path, content):
    try:
        if file_path.startswith("/") or file_path.startswith("../"):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path

        if os.path.isdir(file_abspath) or file_path == None or file_path == "." or file_path == "":
            return f'Error: No path given or is a directory: "{file_path}"'
        else:
            if not os.path.exists(os.path.dirname(file_abspath)):
                os.makedirs(os.path.dirname(file_abspath))
            with open(file_abspath, "w") as open_file:
                open_file.write(content)
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        print("Error:" + str(e))
