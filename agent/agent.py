from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question")

    # call openai
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo" #problem right here until i set the openai key
        messages=[{"role": "user", "content": question}]
    )

    answer = response.choices[0].message["content"]
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)