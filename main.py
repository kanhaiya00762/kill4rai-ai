from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# === Load API key from environment ===
API_KEY = os.getenv("API_KEY")  # Set this in Render's Environment Variables
MODEL = "openai/gpt-3.5-turbo"  # Use a valid model from https://openrouter.ai/docs#models

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/voice", methods=["POST"])
def voice_input():
    data = request.get_json()
    user_text = data.get("text", "")

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://kill4rai-ai.onrender.com",
        "X-Title": "Kill4R-AI"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_text}
        ]
    }

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        result = response.json()
        reply = result["choices"][0]["message"]["content"]
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": f"⚠️ Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
