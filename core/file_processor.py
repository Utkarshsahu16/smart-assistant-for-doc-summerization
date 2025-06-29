import os
from pdfminer.high_level import extract_text

def extract_text_from_file(file):
    if file.type == "application/pdf":
        with open("temp.pdf", "wb") as f:
            f.write(file.read())
        text = extract_text("temp.pdf")
        os.remove("temp.pdf")
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        return "Unsupported file format."
