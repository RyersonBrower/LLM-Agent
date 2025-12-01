from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

AGENT_URL = "http://agent:5001/query"

sources = response_json.get("sources", []) # stored locally for displaying on page
conversation_history.append({
    "question": question,
    "answer": answer,
    "sources": sources
})

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    urls = request.form.get("urls", "")
    files = request.files.getlist("files")

    if not question:
        return jsonify({"history": conversation_history})

    # Build request to agent
    data = {"question": question, "urls": urls}

    files_payload = [
        ("files", (f.filename, f.stream, f.mimetype))
        for f in files
    ]

    try:
        resp = requests.post(AGENT_URL, data=data, files=files_payload)
        response_json = resp.json()
        answer = response_json.get("answer", "(no answer)")
    except Exception as e:
        answer = f"Error contacting agent: {e}"

    # Save to local history
    conversation_history.append({"question": question, "answer": answer})

    return jsonify({"history": conversation_history})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

