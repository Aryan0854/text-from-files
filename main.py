from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
from pdfplumber import open as open_pdf
from docx import Document
import os

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update path

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/extract-text', methods=['POST'])
def extract_text():
    file = request.files['file']
    if file:
        filename = file.filename
        ext = os.path.splitext(filename)[1].lower()
        try:
            if ext in ['.jpg', '.jpeg', '.png']:
                image = Image.open(file)
                text = pytesseract.image_to_string(image)
            elif ext == '.pdf':
                with open_pdf(file) as pdf:
                    text = ''.join(page.extract_text() for page in pdf.pages)
            elif ext == '.docx':
                doc = Document(file)
                text = '\n'.join(paragraph.text for paragraph in doc.paragraphs)
            else:
                return jsonify({'error': 'Unsupported file type'}), 400
            return jsonify({'text': text})
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'error': 'No file uploaded'}), 400

if __name__ == '__main__':
    app.run(debug=True)
