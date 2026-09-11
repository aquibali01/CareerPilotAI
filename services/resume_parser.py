import pdfplumber

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from an uploaded PDF file stream or file path.
    """
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error reading PDF with pdfplumber: {e}")
        return ""
    
    return text.strip()