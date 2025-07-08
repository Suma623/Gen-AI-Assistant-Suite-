from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import json
import google.generativeai as genai

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the Gemini model
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
def load_users():
    if os.path.exists("users.json"):
        with open("users.json", "r") as f:
            users = json.load(f)
            print("Loaded users:", users)  # 👈 Add this line
            return users
    return {}


@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    users = load_users()
    if username in users and users[username] == password:
         return jsonify(status="success")
    return jsonify(status="failure")
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify(status="failure", message="Username and password are required.")

    users = load_users()

    if username in users:
        return jsonify(status="failure", message="Username already exists.")

    users[username] = password
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

    return jsonify(status="success", message="User created successfully.")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    prompt = data.get("prompt", "")

    try:
        response = model.generate_content(prompt)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("✅ Gemini backend running at http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
