import os

def readPromptFile(filePath):
    if os.path.exists(filePath) == False:
        raise FileNotFoundError(f"Prompt file {filePath} does not exist.")
    with open(filePath, 'r', encoding="utf-8") as file:
        content = file.read()
    return content
