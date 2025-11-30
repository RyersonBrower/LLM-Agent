
import json
import os

def load_knowledge(file_path="knowledge/knowledge.json"):
    """Load knowledge from a JSON file."""
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Load knowledge once at import
knowledge = load_knowledge()

def get_relevant_info(query: str) -> str:
    """
    Return knowledge value if the query contains a key from the JSON knowledge.
    Otherwise, return an empty string.
    """
    query = query.lower()
    for key, value in knowledge.items():
        if key.lower() in query:
            return value
    return ""
