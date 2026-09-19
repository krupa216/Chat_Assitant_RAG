import re

input_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\book.txt"
output_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\cleaned_book.txt"

with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()

# Remove extra spaces
text = re.sub(r"[ \t]+", " ", text)

# Remove too many blank lines
text = re.sub(r"\n{3,}", "\n\n", text)

# Keep page markers
text = re.sub(r"\n\s*--- PAGE (\d+) ---\s*\n", r"\n\n--- PAGE \1 ---\n\n", text)

with open(output_file, "w", encoding="utf-8") as file:
    file.write(text.strip())

print("Cleaning completed!")
print("Saved to:", output_file)
print("Characters:", len(text))