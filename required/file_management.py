import os
import re
import shutil

def clean_path(file_path):
    try:
        # Extract the directory and file name from the original file path
        directory, original_file_name = os.path.split(file_path)
        # Extract the file extension
        file_name, file_extension = os.path.splitext(original_file_name)

        # Check if file name is already alphanumeric
        if re.match(r'^[a-zA-Z0-9_]+$', file_name):
            # Return the original path if already alphanumeric
            return file_path
        else:
            # Replace non-alphanumeric characters with underscores
            new_file_name = re.sub(r'[^a-zA-Z0-9]', '_', file_name) + file_extension
            # New file path with alphanumeric name
            new_file_path = os.path.join(directory, new_file_name)

            # Error handling for overwriting
            if os.path.exists(new_file_path):
                raise FileExistsError(f"The file '{new_file_name}' already exists.")

            # Copy the original file to the new file path
            shutil.copy(file_path, new_file_path)

            # Remove the original file
            os.remove(file_path)

    except (FileExistsError, FileNotFoundError, PermissionError) as e:
        # Handle specific errors
        print(f"Error: {e}")
        return file_path
    except Exception as e:
        # Handle any other errors
        print(f"An unexpected error occurred: {e}")
        return file_path
    
    # Return the new file path on success
    return new_file_path
