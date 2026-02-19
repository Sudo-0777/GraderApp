import os
import time
import easyocr
from flask import Flask, request, jsonify, render_template
from werkzeug.utils import secure_filename
from pdf2image import convert_from_path

app = Flask(__name__)

# --- 1. CONFIGURATION ---
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
# UPDATE THIS PATH to your Poppler bin folder
POPPLER_PATH = r"C:\Users\Kalas\Downloads\Release-25.12.0-0\poppler-25.12.0\Library\bin"
ALLOWED_EXTENSIONS = {'pdf'}

for folder in [UPLOAD_FOLDER, PROCESSED_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- 2. INITIALIZE OCR ---
print("--- Loading OCR Engine... ---")
# gpu=False ensures stability on Windows
reader = easyocr.Reader(['en'], gpu=False) 

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_pdf_content(file_path):
    """Converts PDF to images and extracts text using EasyOCR"""
    try:
        pages = convert_from_path(file_path, poppler_path=POPPLER_PATH)
        full_text = []
        
        for i, page in enumerate(pages):
            img_path = os.path.join(PROCESSED_FOLDER, f"temp_page_{i}.jpg")
            page.save(img_path, "JPEG")
            
            # Extract text from the page image
            result = reader.readtext(img_path, detail=0)
            full_text.append(f"Page {i+1}: " + " ".join(result))
            
            # Optional: Remove temp image to save space
            os.remove(img_path) 
            
        return "\n".join(full_text)
    except Exception as e:
        return f"Error processing PDF: {str(e)}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/student', methods=['POST'])
def upload_student():
    if 'file' not in request.files:
        return jsonify({"error": "No file"}), 400
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = f"{time.strftime('%Y%m%d_%H%M%S')}_STUDENT_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # TRIGGER OCR IMMEDIATELY
        extracted_text = process_pdf_content(file_path)
        
        return jsonify({
            "message": "Student file processed",
            "extracted_content": extracted_text
        }), 200

@app.route('/upload/solution', methods=['POST'])
def upload_solution():
    # Add your password check logic here as we did before
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = f"{time.strftime('%Y%m%d_%H%M%S')}_SOLUTION_{secure_filename(file.filename)}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        extracted_text = process_pdf_content(file_path)
        
        return jsonify({
            "message": "Solution key processed",
            "extracted_content": extracted_text
        }), 200

if __name__ == '__main__':
    app.run(debug=True)