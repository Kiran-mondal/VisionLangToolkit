import os
import json
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Enable communication with the Vercel web frontend
CORS(app) 

# --- Your Existing Logic ---

def extract_attributes(image_source, filename=None):
    # Process the in-memory stream directly
    img = Image.open(image_source)
    width, height = img.size
    mode = img.mode

    fname = filename or "stream_upload"

    return {
        "width": width,
        "height": height,
        "mode": mode,
        "filename": fname,
        "timestamp": datetime.now().isoformat()
    }

def classify(attr):
    if attr["width"] > 500:
        return "Large Image"
    else:
        return "Small Image"

def save_to_json(data, output_file="output.json"):
    # Save safely to the root directory
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

# --- Web API Wrapper ---

@app.route('/analyze', methods=['POST'])
def analyze_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    
    # Sanitize the filename
    filename = secure_filename(file.filename)
    if not filename:
        filename = "unnamed_image"

    try:
        # Pass the in-memory stream directly to avoid expensive disk I/O
        # No file.save() beforehand!
        attributes = extract_attributes(file.stream, filename=filename)
        attributes["classification"] = classify(attributes)
        
        # Save output.json to the server
        save_to_json(attributes)
            
        return jsonify(attributes)
        
    except Exception as e:
        error_info = {"error": str(e)}
        return jsonify(error_info), 500

if __name__ == "__main__":
    # Listen on Railway's dynamic PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
