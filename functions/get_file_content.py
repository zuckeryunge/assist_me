import os

def get_file_content(working_directory, file_path=None):
    try:
        if file_path == None or file_path == ".":
            file_abspath = os.path.abspath(working_directory) + "/"
        elif file_path.startswith("/") or file_path.startswith("../"):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        else:
            file_abspath = os.path.abspath(working_directory) + "/" + file_path

        if not os.path.isfile(file_abspath):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        else:
            with open(file_abspath) as open_file:
                file_content_string = open_file.read(10000)
                if len(open_file.read(10001)) == 10001:
                    file_content_string += f'\n[...File "{file_path}" truncated at 10000 characters]'
            return file_content_string  
    except Exception as e:
        print("Error:" + str(e))
