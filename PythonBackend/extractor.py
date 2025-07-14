import sys
import json
from PIL import Image

def extract_attributes(image_path):
    img = Image.open(image_path)
    width, height = img.size
    mode = img.mode
    return {
        "width": width,
        "height": height,
        "mode": mode
    }

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No image path provided"}))
        sys.exit(1)

    path = sys.argv[1]
    try:
        attrs = extract_attributes(path)
        print(json.dumps(attrs))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
