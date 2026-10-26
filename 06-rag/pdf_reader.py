from pypdf import PdfReader

PDF_PATH = "documents/Organic_Shop_HR_Policies_Draft.pdf"

def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    
    full_text = []

    for page in reader.pages:
        text = page.extract_text()

        if text:
            full_text.append(text)

    return "\n\n".join(full_text)
    

if __name__ == "__main__":
    extracted_pages = extract_pdf_text(PDF_PATH)