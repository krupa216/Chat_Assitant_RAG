
import re
import json

from langchain_text_splitters import RecursiveCharacterTextSplitter


# File paths
input_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\cleaned_book.txt"
output_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\chunks.json"


# Read cleaned text
with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()


# Split the book into pages
pages = re.split(r"--- PAGE (\d+) ---", text)


# Remove common PDF extraction noise
def clean_chunk_text(text):
    # Remove .indd filenames
    text = re.sub(r"\S+\.indd", "", text, flags=re.IGNORECASE)

    # Remove date/time patterns such as 13-01-2025 17:32:49
    text = re.sub(
        r"\b\d{1,2}-\d{1,2}-\d{4}\s+\d{1,2}:\d{2}:\d{2}\b",
        "",
        text
    )

    # Remove excessive whitespace
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text.strip()


# Create smaller chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=600,
    chunk_overlap=80,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "? ",
        "! ",
        " ",
        ""
    ]
)


chunks = []


# Process each page
for i in range(1, len(pages), 2):

    page_number = pages[i]
    page_text = pages[i + 1].strip()

    if not page_text:
        continue

    # Clean page text
    page_text = clean_chunk_text(page_text)

    if not page_text:
        continue

    # Split page into smaller chunks
    page_chunks = splitter.split_text(page_text)

    for chunk in page_chunks:

        chunk = clean_chunk_text(chunk)

        if not chunk:
            continue

        chunks.append({
            "page": int(page_number),
            "text": chunk
        })


# Save chunks
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        chunks,
        file,
        ensure_ascii=False,
        indent=2
    )


print("Chunking completed!")
print("Total chunks:", len(chunks))
print("Saved to:", output_file)

