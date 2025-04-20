import pathlib
import textwrap
import google.generativeai as genai
import os
import PyPDF2
from flask import Flask, request, jsonify, render_template
from gtts import gTTS  # For text-to-speech
import uuid  # To generate unique filenames

app = Flask(__name__)

# Configure Google API
GOOGLE_API_KEY = 'AIzaSyCbu-PEJDQTQhgNlf_Q5hKtcBpPQdo38d0'  # Replace with your actual API key
genai.configure(api_key=GOOGLE_API_KEY)

# Select Model
model = genai.GenerativeModel('gemini-1.5-flash')

# Helper function to clean markdown
def to_markdown(text):
    text = text.replace('*', ' ')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

# Function to get Gemini AI Response
def generate_gemini_response(prompt):
    response = model.generate_content(prompt)
    return response.text

# Function to Extract Text from PDF
def extract_text_from_pdf(pdf_file):
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()

# Generate Summary from PDF
@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    pdf_file = request.files.get('pdf_file')

    if not pdf_file:
        return jsonify({'error': 'No PDF file uploaded'}), 400

    extracted_text = extract_text_from_pdf(pdf_file)
    prompt = f"Generate a concise summary of the following text:\n{extracted_text}"
    summary = generate_gemini_response(prompt)

    return jsonify({'summary': summary})

# Convert Summary to Speech
@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.json.get('text')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    tts = gTTS(text, lang='en')
    filename = f"static/audio/{uuid.uuid4()}.mp3"
    tts.save(filename)

    return jsonify({'audio_url': filename})

# Generate Questions and Answers
@app.route('/generate_questions_answers', methods=['POST'])
def generate_questions_answers():
    pdf_file = request.files.get('pdf_file')

    if not pdf_file:
        return jsonify({'error': 'No PDF file uploaded'}), 400

    extracted_text = extract_text_from_pdf(pdf_file)

    prompt = f"Generate 5 questions with their answers based on the following text:\n{extracted_text}"
    questions_answers = generate_gemini_response(prompt)

    return jsonify({'questions_answers': questions_answers})

# Home Route
@app.route('/')
def home():
    return render_template("check.html")

if __name__ == '__main__':
    app.run(debug=True,port=5007)
