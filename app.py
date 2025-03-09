from flask import Flask, render_template, request
import requests

URL = "http://localhost:11434/api/generate"

app = Flask(__name__)

def get_definition(word):
    """Send a word to Ollama and get a friendly definition."""
    prompt = f"Explain the meaning of '{word}' in a friendly, conversational way."
    payload = {
        "model": "llama3.2:3b",  # Use the pulled model
        "prompt": prompt,
        "stream": False  # Get full response at once
    }
    
    try:
        response = requests.post(URL, json=payload)
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.RequestException as e:
        return f"Oops! Something went wrong: {e}"

@app.route("/", methods=["GET", "POST"])
def index():
    """Handle the main page and form submission."""
    definition = None
    word = None
    
    if request.method == "POST":
        word = request.form.get("word", "").strip()
        if word:
            definition = get_definition(word)
    
    return render_template("index.html", word=word, definition=definition)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)