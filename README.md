# VisionLangToolkit

**VisionLangToolkit** is a cross-language visual analysis toolkit. It allows users to extract image-generated attributes using a Unity frontend, a Python backend, and Lua scripting for custom logic.

## 📋 Overview

VisionLangToolkit bridges computer vision and language processing with a comprehensive multi-language architecture. It combines the power of C#, Python, Shell scripts, and Lua to provide a flexible and extensible platform for vision-language applications.

## 🛠️ Tech Stack

- **C#** (55.1%) - Core framework with Unity integration
- **Python** (26.6%) - Backend image analysis and processing
- **Shell** (15.3%) - Automation and deployment scripts
- **Lua** (3%) - Configuration and scripting via MoonSharp

## ✨ Features

- 🎮 **Unity-based UI** for image preview and upload  
- 🐍 **Python Backend** for analyzing image attributes (size, color mode, and more)  
- 🔁 **Lua Scripting** (via MoonSharp) for rule-based logic on attributes  
- 💡 **Modular Architecture** - Easy to extend and integrate with other systems
- 🔧 **Cross-language Support** - Seamless integration between C#, Python, and Lua

## 📦 Requirements

- **Unity** 2020 or newer  
- **Python** 3.6+  
- **Pillow** for Python: `pip install pillow`  
- **MoonSharp** Lua interpreter (for Unity)
- **.NET Runtime** (for C# components)
- **Bash/Shell** (for utility scripts)

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Kiran-mondal/VisionLangToolkit.git
cd VisionLangToolkit
```

### 2. Set Up Python Backend

```bash
cd PythonBackend
pip install -r requirements.txt
python extractor.py path/to/image.jpg
```

### 3. Set Up Unity Project

- Open the project in Unity 2020 or newer
- Install MoonSharp from the Asset Store or via NuGet
- Configure the Python backend connection in the UI settings

### 4. Configure Lua Scripts

- Place your Lua scripts in the designated scripts folder
- Define custom rules and logic in the `.lua` files
- Reference them in the C# components

## 📖 Usage

### Python Image Analysis

```bash
python extractor.py image.jpg
# Outputs: image dimensions, color mode, and other attributes
```

### Unity Frontend

1. Launch the Unity application
2. Use the UI to upload or preview images
3. View extracted attributes and processed results
4. Apply Lua-based transformations as needed

### Lua Scripting

Create custom logic files and configure them in your C# application to process image attributes dynamically.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to:
- Submit a Pull Request
- Report bugs and suggest features via Issues
- Improve documentation and examples

## 📞 Support

For issues, questions, or suggestions, please open an issue on the [GitHub Issues](https://github.com/Kiran-mondal/VisionLangToolkit/issues) page.

## 📈 Project Status

- **Created**: July 14, 2025
- **Last Updated**: May 30, 2026
- **License**: MIT
- **Status**: Active Development

---

Made with ❤️ by [Kiran-mondal](https://github.com/Kiran-mondal)
