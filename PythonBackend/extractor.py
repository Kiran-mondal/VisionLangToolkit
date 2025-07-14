import sys
import json
from PIL import Image
from datetime import datetime
import os

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
    with open(output_file, "w") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    image_path = sys.argv[1]
    try:
        attributes = extract_attributes(image_path)
        attributes["classification"] = classify(attributes)
        save_to_json(attributes)
        print(json.dumps(attributes))  # Optional: print to terminal
    except Exception as e:
        error_info = {"error": str(e)}
        save_to_json(error_info)
        print(json.dumps(error_info))
