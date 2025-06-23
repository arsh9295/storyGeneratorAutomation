from docx import Document
import os

def readDocx(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File does not exist.")

    if not file_path.lower().endswith('.docx'):
        raise ValueError("Only .docx files are supported.")

    try:
        doc = Document(file_path)
        all_text = []
        for para in doc.paragraphs:
            text = para.text.strip()
            if text:
                all_text.append(text)
        return "\n".join(all_text)
    except Exception as e:
        raise RuntimeError(f"Error reading file: {e}")
