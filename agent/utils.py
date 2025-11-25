import json

def load_knowledge(file_path="knowledge/knowledge.json"):
    """Load knowledge from the JSON file"""
    with open(file_path, "r") as f:
        return json.load(f)
    
knowledge = load_knowledge()

def get_relevant_info(query:str):
    """Return knowledge value if query contains a key"""
    query = query.lower()
    for key, value in knowledge.items():
        if key in query:
            return value
    return None