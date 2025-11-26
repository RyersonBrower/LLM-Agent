from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

AGENT_URL = "http://agent:5001/query"  # points to agent container in Docker network

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    question = request.form.get("question")
    if not question:
        return jsonify({"answer": "No question provided."})

    try:
        # Send question to agent service
        response = requests.post(AGENT_URL, json={"question": question})
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
        return jsonify({"answer": f"Error contacting agent: {e}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
