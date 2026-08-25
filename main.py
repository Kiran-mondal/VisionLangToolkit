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

def extract_attributes(image_path):
    img = Image.open(image_path)
    width, height = img.size
    mode = img.mode
    return {
        "width": width,
        "height": height,
        "mode": mode,
        "filename": os.path.basename(image_path),
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
    
    # Save the uploaded file temporarily so your path-based function can read it
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, file.filename)
    file.save(temp_path)

    try:
        # Run your existing pipeline
        attributes = extract_attributes(temp_path)
        attributes["classification"] = classify(attributes)
        
        # Save output.json to the server's local file system
        save_to_json(attributes)
        
        # Clean up the temporary image file to save server storage
        if os.path.exists(temp_path):
            os.remove(temp_path)
            
        return jsonify(attributes)
        
    except Exception as e:
        error_info = {"error": str(e)}
        save_to_json(error_info)
        return jsonify(error_info), 500

if __name__ == "__main__":
    # Listen on Railway's dynamic PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
