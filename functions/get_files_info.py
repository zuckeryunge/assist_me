import os

def get_files_info(working_directory, directory=None):
    if directory == None or directory == ".":
        dir_abspath = os.path.abspath(working_directory + "/")
    elif directory.startswith("/") or directory.startswith("../"):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    else:
        working_abspath = os.path.abspath(working_directory)
        dir_abspath = os.path.join(working_abspath, directory)

    if not os.path.isdir(dir_abspath):
        return f'Error: "{directory}" is not a directory'
    else:
        result = ""
        for item in os.listdir(dir_abspath + "/"):
            item_path = dir_abspath + "/" + item
            description = f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            result = result + description + "\n"
        return result 
 
