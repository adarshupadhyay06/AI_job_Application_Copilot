def extract_text_from_pdf(pdf_path: str) -> str:
    import fitz

    with fitz.open(pdf_path) as document:
        return "\n".join(page.get_text("text") for page in document)
