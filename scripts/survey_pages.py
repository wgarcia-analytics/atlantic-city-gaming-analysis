import os
import pdfplumber

for filename in sorted(os.listdir("data/raw")):
    if not filename.endswith(".pdf"):
        continue
    month = filename.replace(".pdf", "")

    old_page = None
    floor_page = None
    online_page = None

    with pdfplumber.open(f"data/raw/{filename}") as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if "Caesars Interactive NJ" in text and old_page is None:
                old_page = page_number
            if "CASINO WIN COMPARISON" in text and floor_page is None:
                floor_page = page_number
            if "INTERNET GAMING WIN COMPARISON" in text and online_page is None:
                online_page = page_number

    print(month, "| old table:", old_page, "| floor:", floor_page, "| online:", online_page)