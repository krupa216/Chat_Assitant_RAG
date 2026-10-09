import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


# ============================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found.\n"
        "Please create a .env file and add:\n"
        "GEMINI_API_KEY=your_api_key"
    )


# ============================================================
# 2. INITIALIZE GEMINI
# ============================================================

client = genai.Client(api_key=api_key)

# Gemini model used for answer generation
MODEL_NAME = "gemini-3.5-flash"


# ============================================================
# 3. LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Embedding model loaded!")


# ============================================================
# 4. LOAD EXISTING FAISS DATABASE
# ============================================================

print("\nLoading FAISS vector database...")

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS database loaded successfully!")
print("Your 1,604 textbook vectors are ready.")


# ============================================================
# 5. GET USER QUESTION
# ============================================================

question = input(
    "\nAsk a question about the 9th Social Science textbook: "
).strip()

if not question:
    print("Please enter a question.")
    exit()


# ============================================================
# 6. RETRIEVE RELEVANT CHUNKS
# ============================================================

print("\nSearching the textbook...")

results = vectorstore.similarity_search_with_score(
    question,
    k=8
)

print(f"Retrieved {len(results)} relevant chunks.")


# ============================================================
# 7. CREATE CONTEXT FOR GEMINI
# ============================================================

context_parts = []

for i, (document, score) in enumerate(results, start=1):

    page = document.metadata.get("page", "Unknown")

    context_parts.append(
        f"""
==============================
SOURCE {i}
TEXTBOOK PAGE: {page}
DISTANCE SCORE: {score:.4f}
==============================

{document.page_content}
"""
    )

context = "\n".join(context_parts)


# ============================================================
# 8. CREATE RAG PROMPT
# ============================================================

prompt = f"""
You are a research assistant for a Tamil Nadu
9th Standard Social Science textbook.

Your task is to answer the user's question using ONLY
the textbook context provided below.

IMPORTANT RULES:

1. Use only information present in the provided textbook context.

2. Do not use outside knowledge.

3. Do not invent facts.

4. If the answer cannot be found in the provided context,
   say:
   "I could not find this information in the textbook."

5. Give a clear and easy-to-understand answer.

6. When you use information from a textbook page,
   include its page citation in this format:

   [Page 46]

7. If information comes from multiple pages, cite each
   relevant page.

8. Do not mention the internal retrieval process.

9. Do not mention FAISS, MiniLM, embeddings, vector databases,
   or prompts unless the user specifically asks about them.

10. Prefer a concise answer, but include enough explanation
    to properly answer the question.

11. If the retrieved context contains textbook exercise
    questions but does not contain the actual answer,
    do not treat the exercise question itself as evidence
    for an answer.

12. If the evidence is insufficient, clearly say that the
    textbook context provided is insufficient.

------------------------------------------------------------
TEXTBOOK CONTEXT
------------------------------------------------------------

{context}

------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{question}

------------------------------------------------------------

Now answer the user's question using ONLY the textbook
context above.
"""


# ============================================================
# 9. SEND CONTEXT TO GEMINI
# ============================================================

print("\nGenerating answer...")

try:

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            max_output_tokens=1000,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            )
        )
    )

except Exception as e:

    print("\nGemini API error:")
    print(e)
    exit()


# ============================================================
# 10. DISPLAY FINAL ANSWER
# ============================================================

print("\n")
print("=" * 70)
print("ANSWER")
print("=" * 70)

if response.text:
    print(response.text)
else:
    print("Gemini did not return an answer.")


# ============================================================
# 11. DISPLAY RETRIEVED SOURCES
# ============================================================

print("\n")
print("=" * 70)
print("RETRIEVED TEXTBOOK SOURCES")
print("=" * 70)

for i, (document, score) in enumerate(results, start=1):

    page = document.metadata.get("page", "Unknown")

    print(
        f"{i}. Page {page} | "
        f"Distance: {score:.4f}"
    )


print("\n")
