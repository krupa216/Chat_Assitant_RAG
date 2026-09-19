from pypdf import PdfReader

input_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\Documents\9thsocialbook.pdf"
output_file = output_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\book.txt"

reader = PdfReader(input_file)

print("Total pages:", len(reader.pages))

with open(output_file, "w", encoding="utf-8") as file:

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text()

        if text:
            file.write(f"\n--- PAGE {page_number} ---\n")
            file.write(text)
            file.write("\n")

print("Text extraction completed!")
print("Saved to:", output_file)