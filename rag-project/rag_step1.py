import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the embedding model

model = SentenceTransformer('all-MiniLM-L6-v2')

def chunk_text(text, chunk_size=20, overlap=5):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i = i + chunk_size - overlap
    return chunks


# Build the VDB to store the vectors from ^^ steps

def build_faiss_index(chunks):
    print("Embedding chunks and building FAISS index...")
    embeddings = model.encode(chunks, convert_to_numpy=True)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    print("Adding vectors to FAISS index ..")
    index.add(embeddings)
    return index,embeddings

# Search function (top-k)

def search(query, chunks, index, embeddings, top_k):
    print("\nSearching for:", query)
    query_vec = model.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_vec, top_k)
    results = []
    for idx in indices[0]:
        results.append(chunks[idx])
    return results

if __name__ == "__main__":
    # Sample text (replace with your own)
    text = """
    The Indian Premier League has seen a variety of champions over the years, each season producing its own memorable storyline. Chennai Super Kings have been one of the most successful teams, winning titles in 2010, 2011, 2018, 2021, and again in 2023 under the leadership of MS Dhoni. Mumbai Indians, led by Rohit Sharma, have also dominated the league with victories in 2013, 2015, 2017, 2019, and 2020, making them the team with the highest number of IPL trophies. Kolkata Knight Riders claimed the championship in 2012 and 2014, both times under Gautam Gambhir’s captaincy. Sunrisers Hyderabad lifted the trophy in 2016 after a strong season led by David Warner, while Rajasthan Royals were the inaugural champions in 2008 under Shane Warne. Gujarat Titans, a new franchise, surprised everyone by winning the 2022 season in their debut year with Hardik Pandya as captain. With so many different winners across different eras, any retrieval system must correctly interpret queries about IPL champions by understanding the year, the team, and the context behind each victory.
    """
    
    # Step 1: Chunk the text
    chunks = chunk_text(text, chunk_size=20)
    print("Text has been chunked into the following pieces:")
    for c in chunks:
        print("-", c)
    
    # Step 2: Build the FAISS index
    index, embeddings = build_faiss_index(chunks)
    
    # Step 3: Search for a query
    query = "How many times has CSK won the IPL?"
    results = search(query, chunks, index, embeddings, top_k=8)
    
    print("\nTop Results:")
    for r in results:
        print("-", r)