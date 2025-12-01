from flask import Flask, request, jsonify
from openai import OpenAI
from utils import get_relevant_info
import os
import requests
from bs4 import BeautifulSoup
from docx import Document
from pypdf import PdfReader

# Initialize OpenAI client (requires OPENAI_API_KEY in env)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

# ------------------- Short-term memory --------------------
chat_history = []
used_sources = []
MAX_HISTORY = 6


def append_to_history(role, text):
    chat_history.append({"role": role, "content": text})
    if len(chat_history) > MAX_HISTORY:
        del chat_history[:-MAX_HISTORY]

# ------------------- File / URL extraction --------------------
def extract_pdf(file):
    reader = PdfReader(file)
    return "\n".join([page.extract_text() or "" for page in reader.pages])

def extract_txt(file):
    return file.read().decode("utf-8")

def extract_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_url(url):
    try:
        html = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html, "html.parser")
        return soup.get_text(separator="\n")
    except:
        return ""

# ------------------- Simple retrieval (optional) --------------------
def simple_retrieval(text, question):
    """Return lines containing any words from the question."""
    q_words = question.lower().split()
    return "\n".join([line for line in text.split("\n") if any(w in line.lower() for w in q_words)])

# ------------------- /query route --------------------
@app.route("/query", methods=["POST"])
def query():
    used_sources.clear()

    # Accept FormData or JSON
    if request.is_json:
        data = request.json
        files = []
    else:
        data = request.form
        files = request.files.getlist("files")

    question = data.get("question", "").strip()
    urls = data.get("urls", "").strip()

    if not question:
        return jsonify({"answer": "Missing question"})

    # ------------------- Extract text from files --------------------
    full_text = ""
    for f in files:
        if f.filename.endswith(".pdf"):
            full_text += extract_pdf(f) + "\n"
            used_sources.append({"type": "file", "name": f.filename})
        elif f.filename.endswith(".txt"):
            full_text += extract_txt(f) + "\n"
            used_sources.append({"type": "file", "name": f.filename})
        elif f.filename.endswith(".docx") or f.filename.endswith(".doc"):
            full_text += extract_docx(f) + "\n"
            used_sources.append({"type": "file", "name": f.filename})

    # ------------------- Extract text from URLs --------------------
    # ------------------- Extract text from URLs --------------------
    if urls:
        for url in urls.split(","):
            url = url.strip()
            if url:
                full_text += extract_url(url) + "\n"
                used_sources.append({"type": "url", "name": url})


    # ------------------- Add JSON knowledge --------------------
    json_knowledge = get_relevant_info(question)
    if json_knowledge:
        full_text += "\n" + json_knowledge

    # ------------------- Optional simple retrieval --------------------
    context = simple_retrieval(full_text, question)
    if not context:
        context = full_text[:4000]  # fallback

    # ------------------- Append to chat memory --------------------
    append_to_history("user", question)

    messages = [
        {"role": "system", "content": "Answer using only the provided context."},
        *chat_history,
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"}
    ]

    # ------------------- Call OpenAI --------------------
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        answer = response.choices[0].message.content
    except Exception as e:
        answer = f"LLM Error: {e}"

    append_to_history("assistant", answer)

    return jsonify({
        "answer": answer,
        "sources": used_sources
})

# ------------------- Reset memory --------------------
@app.route("/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "cleared"})

# ------------------- Run app --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)




