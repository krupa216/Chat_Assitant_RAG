import re

input_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\book.txt"
output_file = r"C:\Users\Lenovo\Desktop\rag-research assistant\extracted_text\cleaned_book.txt"


# Read original extracted text
with open(input_file, "r", encoding="utf-8") as file:
    text = file.read()


# --------------------------------------------------
# Convert literal \n into real newlines
# --------------------------------------------------

text = text.replace("\\n", "\n")


# --------------------------------------------------
# Remove .indd filenames
# --------------------------------------------------

text = re.sub(
    r"\S*\.indd",
    "",
    text,
    flags=re.IGNORECASE
)


# --------------------------------------------------
# Remove dates and times
# --------------------------------------------------

text = re.sub(
    r"\b\d{1,2}-\d{1,2}-\d{4}\b",
    "",
    text
)

text = re.sub(
    r"\b\d{1,2}:\d{2}:\d{2}\b",
    "",
    text
)


# --------------------------------------------------
# Remove URLs
# --------------------------------------------------

text = re.sub(
    r"https?://\S+",
    "",
    text,
    flags=re.IGNORECASE
)

text = re.sub(
    r"www\.\S+",
    "",
    text,
    flags=re.IGNORECASE
)


# --------------------------------------------------
# Remove repeated textbook front-matter information
# --------------------------------------------------

remove_phrases = [
    "GOVERNMENT OF TAMIL NADU",
    "Government of Tamil Nadu",
    "Department of School Education",
    "publication under Free Textbook Programme",
    "Free Textbook Programme",
    "STANDARD NINE",
    "First Edition - 2018",
    "First Edition - 2018",
    "Revised Edition - 2019, 2020, 2022, 2023, 2025",
    "Reprint - 2021, 2024",
    "Published under New Syllabus",
    "Tamil Nadu Textbook and Educational Services Corporation",
    "State Council of Educational Research and Training",
    "SCERT 2018",
    "Printing & Publishing",
    "Content Creation",
    "NOT FOR SALE"
]

for phrase in remove_phrases:
    text = re.sub(
        re.escape(phrase),
        "",
        text,
        flags=re.IGNORECASE
    )


# --------------------------------------------------
# Remove helpline information
# --------------------------------------------------

text = re.sub(
    r"Dial\s*\d{3,}",
    "",
    text,
    flags=re.IGNORECASE
)

text = re.sub(
    r"\b\d{10,12}\b",
    "",
    text
)

remove_helpline = [
    "toll free",
    "helplines for children below 18 years",
    "if you are forced into child marriage or child labour",
    "if you are emotionally, physically, sexually harassed or abused",
    "if you are feeling threatened",
    "if you feel unsafe",
    "caller details will be kept confidential",
    "if you need guidance for examinations or Higher Education"
]

for phrase in remove_helpline:
    text = re.sub(
        re.escape(phrase),
        "",
        text,
        flags=re.IGNORECASE
    )


# --------------------------------------------------
# Remove standalone Roman numeral page numbers
# --------------------------------------------------

text = re.sub(
    r"(?m)^\s*[IVXLCDM]{1,6}\s*$",
    "",
    text
)


# --------------------------------------------------
# Remove standalone numbers
# --------------------------------------------------

text = re.sub(
    r"(?m)^\s*\d{1,4}\s*$",
    "",
    text
)


# --------------------------------------------------
# Clean spaces
# --------------------------------------------------

text = re.sub(
    r"[ \t]+",
    " ",
    text
)

text = re.sub(
    r"\n\s*\n\s*\n+",
    "\n\n",
    text
)


# --------------------------------------------------
# Preserve page markers
# --------------------------------------------------

text = re.sub(
    r"\s*--- PAGE\s+(\d+)\s*---\s*",
    r"\n\n--- PAGE \1 ---\n\n",
    text
)


# --------------------------------------------------
# Save
# --------------------------------------------------

text = text.strip()

with open(output_file, "w", encoding="utf-8") as file:
    file.write(text)


print("Cleaning completed!")
print("Saved to:", output_file)
print("Characters:", len(text))