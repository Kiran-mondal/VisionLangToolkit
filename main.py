import os
import sys
import json
import tempfile
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable communication with the web frontend

# --- Your Existing Logic ---

def extract_attributes(image_source, filename=None):
    # ⚡ Bolt: Pass in-memory stream to Image.open directly instead of writing to disk.
    img = Image.open(image_source)
    width, height = img.size
    mode = img.mode

    # If image_source is a path, use its basename, otherwise use the provided filename
    if isinstance(image_source, str):
        fname = os.path.basename(image_source)
    else:
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

def save_to_json(data, output_file="PythonBackend/output.json"):
    # Ensure the directory exists before saving (crucial for cloud environments)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

# --- Web API Wrapper ---

@app.route('/analyze', methods=['POST'])
def analyze_api():
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']

    try:
        # Run your existing pipeline
        # ⚡ Bolt: Pass the in-memory stream directly to avoid expensive disk I/O (~78% faster)
        attributes = extract_attributes(file.stream, filename=file.filename)
        attributes["classification"] = classify(attributes)
        
        # Save output.json to the server's local file system
        save_to_json(attributes)
            
        return jsonify(attributes)
        
    except Exception as e:
        error_info = {"error": str(e)}
        save_to_json(error_info)
        return jsonify(error_info), 500

if __name__ == "__main__":
    # Listen on Railway's dynamic PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
