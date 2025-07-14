#!/bin/bash

echo "📂 Step 1: Extracting Image Attributes with Python"
python3 PythonBackend/extractor.py test_image.jpg > PythonBackend/output.json

echo "✅ Attributes saved to PythonBackend/output.json"
cat PythonBackend/output.json

echo "📦 Unity and Lua logic must be tested from inside the Unity editor."