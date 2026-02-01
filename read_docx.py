from docx import Document
import sys

def read_docx(filename):
    try:
        doc = Document(filename)
        print(f"--- Content of {filename} ---")
        for para in doc.paragraphs:
            print(para.text)
        print("--- End of Content ---")
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        read_docx(sys.argv[1])
    else:
        # Default for this debugging session
        read_docx("Cover_Letter_New_Plymouth_District_Council_Development_Engineer.docx")
