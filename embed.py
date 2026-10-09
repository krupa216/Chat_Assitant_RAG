import json

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

# Load chunks
with open("extracted_text/chunks.json", "r", encoding="utf-8") as file:
    chunks = json.load(file)

print("Total chunks:", len(chunks))

# Convert chunks into documents
documents = []

for chunk in chunks:
    documents.append(
        Document(
            page_content=chunk["text"],
            metadata={"page": chunk["page"]}
        )
    )

print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

print("Creating embeddings and FAISS index...")

vectorstore = FAISS.from_documents(
    documents,
    embeddings
)

# Save FAISS database
vectorstore.save_local("vectorstore")

print("Embedding and vector database creation completed!")
print("Total vectors:", len(documents))
print("Saved to: vectorstore/")