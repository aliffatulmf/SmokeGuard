import logging
import os
import shutil


def delete_cache(exclude=[], verbose=False):
    exclude.extend([".git", ".vscode"])  # Adding ".git" and ".vscode" to exclude
    extensions = ['__pycache__', '.pyc', '.pyd', '.pyo']
    
    for root, dirs, files in os.walk(os.getcwd()):
        for name in files:
            if any(name.endswith(ext) for ext in extensions) and name not in exclude:
                file_path = os.path.join(root, name)
                if os.path.isfile(file_path):  # Verifying that this is a file
                    try:
                        os.remove(file_path)
                        if verbose:
                            logging.info(f'[red]Deleted[/red] {file_path}')
                    except Exception as e:
                        logging.error(f'Failed to delete file {file_path}. Error: {e}')
        
        for name in dirs:
            if any(name.endswith(ext) for ext in extensions) and name not in exclude:
                dir_path = os.path.join(root, name)
                if os.path.isdir(dir_path):  # Verifying that this is a directory
                    try:
                        shutil.rmtree(dir_path)
                        if verbose:
                            logging.info(f'[red]Deleted[/red] {dir_path}')
                    except Exception as e:
                        logging.error(f'Failed to delete directory {dir_path}. Error: {e}')
                        
    logging.info("Cache deleted successfully")