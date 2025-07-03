import os

def getAllFilesInProvidedPath(directory, extensions=None):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if extensions:
                if any(file.lower().endswith(ext.lower()) for ext in extensions):
                    file_paths.append(os.path.join(root, file))
            else:
                file_paths.append(os.path.join(root, file))
    return file_paths
