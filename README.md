# VisionLangToolkit

**VisionLangToolkit** is a cross-language visual analysis toolkit. It allows users to extract image-generated attributes using a Unity frontend, a Python backend, and Lua scripting for custom logic. This modular tool is great for education, research, and experimental automation.

---

## ✨ Features

- 🎮 Unity-based UI for image preview and upload  
- 🐍 Python script for analyzing image attributes (size, color mode)  
- 🔁 Lua scripting (via MoonSharp) for rule-based logic on attributes  
- 💡 Modular and cross-language (C# + Python + Lua)

---

## 🔧 Requirements

- Unity 2020 or newer  
- Python 3.6+  
- Pillow for Python: `pip install pillow`  
- MoonSharp Lua interpreter (for Unity)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone
https://github.com/Kiran-mondal/VisionLangToolkit.git
cd VisionLangToolkit

cd PythonBackend
python extractor.py path/to/image.jpg
