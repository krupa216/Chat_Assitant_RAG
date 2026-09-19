import re
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter


input_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\cleaned_book.txt"
output_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\chunks.json"


# Read cleaned text
with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()


# Split the book into pages
pages = re.split(r"--- PAGE (\d+) ---", text)


# Create text splitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=150
)


chunks = []


# Process each page
for i in range(1, len(pages), 2):

    page_number = pages[i]
    page_text = pages[i + 1].strip()

    if not page_text:
        continue

    page_chunks = splitter.split_text(page_text)

    for chunk in page_chunks:

        chunks.append({
            "page": int(page_number),
            "text": chunk
        })


# Save chunks
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(chunks, file, ensure_ascii=False, indent=2)


print("Chunking completed!")
print("Total chunks:", len(chunks))
print("Saved to:", output_file)