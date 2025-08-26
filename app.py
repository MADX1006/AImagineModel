# Save this file as app.py
import os
from flask import Flask, render_template, request, jsonify, Response
from werkzeug.utils import secure_filename
import google.generativeai as genai

# Initialize Flask app
app = Flask(__name__)

# Set upload folder
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set your Gemini API key
# The API key has been updated as requested.
genai.configure(api_key="AIzaSyCHZa7s34WE-W7VmqdtRPb5hZ4LNe8Wg_c")

@app.route('/')
def index():
    """Renders the main page of the application."""
    # Assuming there's an index.html in a 'templates' folder.
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """
    Handles file upload, analyzes the document using the Gemini API, and returns the analysis.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        document_content = f.read()

    prompt = f"""
    You are an expert cybersecurity analyst. Your task is to perform a security analysis on the following project document.
    Please identify potential vulnerabilities, threats, and security risks. For each identified risk, suggest a practical test case to verify its existence.
    For each test case, mark it as 'Checked' if it is relevant and explain briefly.

    Document for analysis:
    ---
    {document_content}
    ---

    Provide your analysis as a JSON array like:
    [
      {{ "test_case": "...", "status": "Checked", "explanation": "..." }},
      ...
    ]
    """

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(prompt)
        # Try to extract JSON from Gemini's response
        import json
        import re
        match = re.search(r'\[.*\]', response.text, re.DOTALL)
        if match:
            test_cases = json.loads(match.group(0))
        else:
            test_cases = []

        return jsonify({'test_cases': test_cases})
    except Exception as e:
        return jsonify({'error': f'Gemini API Error: {str(e)}'}), 500
    finally:
        os.remove(filepath)

@app.route('/chat', methods=['POST'])
def chat():
    """
    Handles live chat messages, sending them to Gemini and streaming the response back.
    """
    data = request.json
    message = data.get('message', '')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
        response = model.generate_content(message)
        reply = response.text
        return reply, 200
    except Exception as e:  
        return f'Gemini API Error: {str(e)}', 500

if __name__ == '__main__':
    # Make sure to run the Flask app on 0.0.0.0 for external access
    app.run(host='0.0.0.0', port=8000)
