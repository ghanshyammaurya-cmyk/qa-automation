import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page_num, page in enumerate(doc, start=1):
            text += f"\n--- Page {page_num} ---\n"
            text += page.get_text()
    return text

def compare_pdfs(pdf1_path, pdf2_path):
    """Compare two PDF files and show line-by-line differences."""
    text1 = extract_text_from_pdf(pdf1_path).splitlines()
    text2 = extract_text_from_pdf(pdf2_path).splitlines()

    max_lines = max(len(text1), len(text2))
    differences = []

    for i in range(max_lines):
        line1 = text1[i] if i < len(text1) else ""
        line2 = text2[i] if i < len(text2) else ""
        if line1.strip() != line2.strip():
            differences.append((i + 1, line1, line2))

    if differences:
        print("Differences found:\n")
        for line_num, line1, line2 in differences:
            print(f"Line {line_num}:\n  PDF1: {line1}\n  PDF2: {line2}\n")
    else:
        print("The PDFs are identical.")

# Example usage

compare_pdfs(
    r"C:\Users\onsumaye\PycharmProjects\PythonProject1\critical-infrastructure-sap-brief.pdf",
    r"C:\Users\onsumaye\PycharmProjects\PythonProject1\critical-infrastructure-intelligence-packages-from-sap-powered-by-intel-1760609961.pdf"
)
