<div align="center">
  <img src="VisionLangWeb/visionlangtoolkit_logo.svg" alt="VisionLangToolkit Logo" width="250" style="border-radius: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1);" />
  
#  VisionLangToolkit

  **Advanced Image Analysis & Color Extraction Tool**

  [![Frontend deployment](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)](#)
  [![Backend deployment](https://img.shields.io/badge/Backend-Railway-purple?logo=railway)](#)
  [![Python version](https://img.shields.io/badge/Python-3.9+-blue.svg?logo=python)](#)
</div>

## 📌 About The Project

🎯 VisionLangToolkit is a professional web-based SaaS application designed to process and analyze images seamlessly. It extracts technical metadata such as resolution, format, aspect ratio, and orientation.

The platform includes a responsive user interface, secure authentication (GitHub OAuth & Email), and an interactive live mobile preview section.

## ✨ Features

- 📊 **Image Metadata Extraction:** Instantly retrieves File Size, Resolution, Format (PNG/JPG/WEBP), Orientation (Landscape/Portrait), and Aspect Ratio.
- 🎨 **Smart Color Palette:** Identifies the top 5 dominant colors from the uploaded image and fetches their exact names using `TheColorAPI`.
- 📋 **Click-to-Copy Hex Codes:** Interactive color swatches that allow users to copy hex codes to their clipboard instantly.
- 🔐 **Authentication System:** Integrated GitHub OAuth and Email-based dummy registration flows.
- 📱 **Live iPhone Preview:** Embedded interactive iPhone mockup frame to test game/project URLs directly within the dashboard.
- 💾 **Export Data:** Option to export the analyzed image metadata as a JSON file.

## 🛠️ Tech Stack

**🖥️ Frontend:**
- 🌐 HTML5, Vanilla JavaScript
- 🎨 Tailwind CSS (via CDN)
- ☁️ Hosted on **Vercel**

**⚙️ Backend:**
- 🐍 Python, Flask
- 🖼️ Pillow (PIL) for image processing
- 🔑 Authlib (for GitHub OAuth integration)
- ☁️ Hosted on **Railway**

## 🚀 Quick Start

### 🌐 Live Demo
👉 **[Try VisionLangToolkit Now](https://visionlangtoolkit.quarry.dpdns.org/)**

## 💻 Local Installation

### 📥 Clone & Setup:
```bash
git clone https://github.com/Kiran-mondal/VisionLangToolkit.git
cd VisionLangToolkit
pip install -r requirements.txt
python main.py
```

### ⚙️ Configuration:
Create a `.env` file and add your GitHub Client ID & Secret:
```env
GITHUB_CLIENT_ID=your_client_id
GITHUB_CLIENT_SECRET=your_client_secret
```

### 🖥️ Frontend Setup:
Simply open `index.html` in your favorite web browser or use a live server extension in VS Code.

## 📖 API Documentation

VisionLangToolkit offers a RESTful API endpoint for image analysis. See documentation for detailed endpoint specifications.

### 📊 Core Endpoints:
- 🔍 `/analyze` - Image metadata extraction
- 🎨 `/colors` - Dominant color detection
- 📥 `/upload` - Secure image upload

## 📦 Language Composition

- 🌐 HTML: 78.1%
- 🐍 Python: 15%
- 💻 C#: 5.1%
- 🔧 Shell: 1.4%

## 📝 License

© 2026 VisionLangToolkit. All rights reserved.

---

<div align="center">
  <p>Made with ❤️ by Kiran Mondal</p>
</div>
