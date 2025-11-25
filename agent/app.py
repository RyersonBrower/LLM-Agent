from flask import Flask, request, jsonify
from openai import OpenAI
from utils import get_relevant_info
import os


client = OpenAI()
app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")

    info = get_relevant_info

    if info:
        prompt = f"You are an intelligent agent. Use this info to answer the question"
    else:
        prompt = f"You are an intelligent agent. Answer the following question: {question}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )

    answer = response.choices[0].message.content
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)



    