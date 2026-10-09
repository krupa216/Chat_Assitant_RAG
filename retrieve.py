
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# 1. Load the embedding model
print("Loading embedding model...")

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# 2. Load the saved FAISS vector database
print("Loading FAISS database...")

vectorstore = FAISS.load_local(
    "vectorstore",
    embeddings,
    allow_dangerous_deserialization=True
)

print("FAISS vector database loaded!")
print("Number of documents:", vectorstore.index.ntotal)


# 3. Ask one question
question = input("\nAsk a question: ")

print("\nYou entered:", question)
print("Searching FAISS...")


# 4. Retrieve top 5 results WITH similarity scores
results = vectorstore.similarity_search_with_score(
    question,
    k=5
)


print("Search completed!")
print("Number of results:", len(results))


# 5. Display the results
print("\n--- Retrieved Results ---\n")


for i, (result, score) in enumerate(results, start=1):

    print(f"Result {i}")
    print(f"Page: {result.metadata.get('page')}")
    print(f"Score: {score}")
    print("Text:")
    print(result.page_content[:800])
    print("-" * 60)

