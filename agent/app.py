from flask import Flask, request, jsonify
from openai import OpenAI
from utils import get_relevant_info
import os

client = OpenAI()
app = Flask(__name__)

# ------------------- Short term memory --------------------
chat_history = []
MAX_HISTORY = 6

def append_to_history(role, text):
    chat_history.append({"role": role, "content": text})
    if len(chat_history) > MAX_HISTORY:
        del chat_history[:-MAX_HISTORY]

def build_messages(system_text, question):
    messages = [{"role": "system", "content": system_text}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": question})
    return messages

# ------------------- ROUTES --------------------
@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    info = get_relevant_info(question)

    if info:
        system_text = f"You are an intelligent agent. Use this knowledge to help answer: {info}"
    else:
        system_text = "You are an intelligent agent. Answer clearly."

    # Save user message
    append_to_history("user", question)

    # Build messages list
    messages = build_messages(system_text, question)

    # ---- Correct OpenAI API for your version ----
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Extract answer
    answer = response.choices[0].message.content

    # Save assistant reply
    append_to_history("assistant", answer)

    return jsonify({"answer": answer})

@app.route("/reset", methods=["POST"])
def reset():
    chat_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

