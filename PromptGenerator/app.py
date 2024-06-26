from flask import Flask, request, jsonify, send_file, send_from_directory
import os
import google.generativeai as genai

app = Flask(__name__)

# Directly set the API key for testing purposes
API_KEY = "AIzaSyCodKCC1sCFo-4F2rU7UlNvU0b9Ogb8jUs"

# Configure the Generative AI with the API key
genai.configure(api_key=API_KEY)

# Create the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "I want you to become my Prompt Creator. Your goal is to help me craft the best possible prompt for my needs. "
        "The prompt will be used by you. You will follow the following process: 1. Your first response will be to ask "
        "me what the prompt should be about. I will provide my answer, but we will need to improve it through continual "
        "iterations by going through the next steps. 2. Based on my input, you will generate 3 sections. a) Revised prompt "
        "(provide your rewritten prompt. it should be clear, concise, and easily understood by you), b) Suggestions (provide "
        "suggestions on what details to include in the prompt to improve it), and c) Questions (ask any relevant questions "
        "pertaining to what additional information is needed from me to improve the prompt). 3. We will continue this iterative "
        "process with me providing additional information to you and you updating the prompt in the Revised prompt section until it's complete."
    ),
)

history = []

# Serve index.html from the root path
@app.route('/')
def index():
    return send_file('index.html')

# Serve static files (styles.css and script.js)
@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('.', path)

# Handle chat interactions
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']

    chat_session = model.start_chat(
        history=history
    )

    response = chat_session.send_message(user_input)
    model_response = response.text

    # Append user input and model response to history
    history.append({"role": "user", "parts": [{"text": user_input}]})
    history.append({"role": "model", "parts": [{"text": model_response}]})

    return jsonify({"response": model_response})

if __name__ == '__main__':
    app.run(debug=True)