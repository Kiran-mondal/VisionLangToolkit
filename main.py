import os
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. Apply configs at the TOP so Railway's gunicorn actually reads them
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Allow up to 16MB files

# 2. Properly initialize CORS for the entire app
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Online", "message": "API is running!"})

@app.route('/analyze', methods=['POST'])
def analyze_api():
    try:
        if 'image' not in request.files:
            print("ERROR: No image found in request.")
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']

        # Security: Validate input content type
        if not file.content_type or not file.content_type.startswith('image/'):
            print("ERROR: Invalid file type.")
            return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

        filename = secure_filename(file.filename) or "unnamed_image"
        print(f"Receiving file: {filename}")

        # Process the image in memory
        img = Image.open(file.stream)
        width, height = img.size
        print(f"Image processed successfully: {width}x{height}")
        
        attributes = {
            "width": width,
            "height": height,
            "mode": img.mode,
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        
        attributes["classification"] = "Large Image" if width > 500 else "Small Image"
            
        return jsonify(attributes)
        
    except Exception as e:
        # Print the exact error to the Railway logs
        print(f"CRITICAL ERROR: {str(e)}")
        # Security: Do not leak error details to the client
        return jsonify({"error": "An internal processing error occurred"}), 500
        
