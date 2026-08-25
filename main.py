import os
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
# Force CORS to allow ALL traffic from ANY website
CORS(app, resources={r"/*": {"origins": "*"}})

# --- HEALTH CHECK ROUTE ---
# This lets you test if the server is awake in your mobile browser
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "status": "Online", 
        "message": "VisionLangToolkit API is running! Send images via POST to /analyze"
    })

# --- MAIN ANALYSIS ROUTE ---
@app.route('/analyze', methods=['POST', 'OPTIONS'])
def analyze_api():
    # Handle browser security preflight checks
    if request.method == 'OPTIONS':
        return jsonify({}), 200 
        
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files['image']
    filename = secure_filename(file.filename) or "unnamed_image"

    try:
        # Process the image completely in memory (No disk saving)
        img = Image.open(file.stream)
        width, height = img.size
        
        attributes = {
            "width": width,
            "height": height,
            "mode": img.mode,
            "filename": filename,
            "timestamp": datetime.now().isoformat()
        }
        
        if width > 500:
            attributes["classification"] = "Large Image"
        else:
            attributes["classification"] = "Small Image"
            
        return jsonify(attributes)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
