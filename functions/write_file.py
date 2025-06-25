import os

def write_file(working_directory, file_path, content):
    try:
        if file_path == None or file_path == "." or file_path == "":
            file_abspath = os.path.abspath(working_directory) + "/"
        elif file_path.startswith("/") or file_path.startswith("../"):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path

        if not os.path.isfile(file_abspath) or file_path == None or file_path == ".":
            return f'Error: No path given or is a directory: "{file_path}"'
        else:
            # chheck if path exists
                # if not create dir AND file
                # if does write to file
            # when success return success message
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'  
    except Exception as e:
        print("Error:" + str(e))
