import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2') 

text_folder_path = 'master'

def load_text_files(folder_path):
    texts = []
    filenames = []
    
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                texts.append(file.read())
                filenames.append(filename)
    
    return texts, filenames

texts, filenames = load_text_files(text_folder_path)

embeddings = model.encode(texts, convert_to_tensor=False)

dimension = embeddings.shape[1]  
index = faiss.IndexFlatL2(dimension) 

embeddings = np.array(embeddings).astype('float32')
index.add(embeddings)  

faiss.write_index(index, 'faiss_index.bin')

def search(query, top_k=10):
    query_embedding = model.encode([query], convert_to_tensor=False)
    query_embedding = np.array(query_embedding).astype('float32')
    
    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for i in range(top_k):
        result = {
            'filename': filenames[indices[0][i]],
            'text_snippet': texts[indices[0][i]][:1000], 
            'distance': distances[0][i]
        }
        results.append(result)
    
    return results

query = "suspected vessel"
top_k_results = search(query, top_k=5)

for i, result in enumerate(top_k_results):
    print(f"Result {i+1}:")
    print(f"Filename: {result['filename']}")
    print(f"Text Snippet: {result['text_snippet']}...")
    print(f"Distance: {result['distance']}")
    print("-" * 50)
