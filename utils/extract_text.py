import PyPDF2

def extract_text_from_pdf(pdf_file):
    with pdf_file as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
