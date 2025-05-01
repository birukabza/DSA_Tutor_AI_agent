import chromadb
import os
import hashlib
from chromadb.utils import embedding_functions





class ProblemDBManager:
    def __init__(self, collection_name="dsa_problems"):
        ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-ada-002",
            )
        
        db_path = os.getenv('CHROMA_DB_PATH', './chroma_db')

        self.client = chromadb.PersistentClient(path=db_path)
        
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=ef,
            metadata={"distance_metric": "cosine"}
        )
        
    
    def add_problem(self, problem_text, difficulty, topic):
        problem_id = hashlib.md5(problem_text.encode()).hexdigest()
        
        self.collection.add(
            documents=[problem_text],
            metadatas=[{"difficulty": difficulty, "topic": topic}],
            ids=[problem_id]
        )
        return problem_id
    
    def get_similar_problems(self, query_text, n_results=1, difficulty=None):
        query_kwargs = {
            "query_texts": [query_text],
            "n_results": n_results,
        }
        if difficulty:
            query_kwargs["where"] = {"difficulty": difficulty}

        results = self.collection.query(**query_kwargs)
        similar = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            similar.append({
                "problem": doc,
                "difficulty": meta.get("difficulty"),
                "topic": meta.get("topic"),
                "similarity": dist,
            })
        return similar

    
    def is_problem_exists(self, problem_text):
        problem_id = hashlib.md5(problem_text.encode()).hexdigest()
        results = self.collection.get(ids=[problem_id])
        return len(results["documents"]) > 0