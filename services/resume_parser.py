import pdfplumber
import PyPDF2

def extract_text_from_pdf(pdf_file) -> str:
    """
    Extracts raw text from an uploaded PDF file stream or file path.
    Uses pdfplumber as primary extractor with PyPDF2 as fallback.
    """
    text = ""
    # 1. Try pdfplumber first
    try:
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"[resume_parser] pdfplumber error: {e}")

    text = text.strip()
    if len(text) > 20:
        return text

    # 2. Fallback to PyPDF2 if pdfplumber returned empty or very short text
    try:
        if hasattr(pdf_file, "seek"):
            pdf_file.seek(0)
        reader = PyPDF2.PdfReader(pdf_file)
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    except Exception as e:
        print(f"[resume_parser] PyPDF2 error: {e}")

    return text.strip()