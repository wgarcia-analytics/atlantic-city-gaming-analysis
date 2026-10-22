import pdfplumber

filename = "data/raw/2017-01.pdf"

with pdfplumber.open(filename) as pdf:
    print("Pages:", len(pdf.pages))

    for page_number, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ""
        for line in text.split("\n"):
            if "Win" in line or "Wagering" in line or "Total Gaming" in line:
                print(f"Page {page_number}: {line}")