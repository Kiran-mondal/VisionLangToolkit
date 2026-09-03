import os
import math
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix 
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)

# Railway-এর Proxy ঠিক করার জন্য
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  
app.secret_key = os.environ.get("SECRET_KEY", "vision_toolkit_secret_key")

# SECURITY: Restrict CORS
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1,https://visionlangtoolkit.quarry.dpdns.org").split(",")
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Online", "message": "API is running!"})

# ==========================================
# GITHUB OAUTH SETUP
# ==========================================
oauth = OAuth(app)
github = oauth.register(
    name='github',
    client_id=os.environ.get("GITHUB_CLIENT_ID"),
    client_secret=os.environ.get("GITHUB_CLIENT_SECRET"),
    access_token_url='https://github.com/login/oauth/access_token',
    access_token_params=None,
    authorize_url='https://github.com/login/oauth/authorize',
    authorize_params=None,
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

@app.route('/login/github')
def login_github():
    redirect_uri = "https://visionlangtoolkit-production.up.railway.app/auth/github/callback"
    return github.authorize_redirect(redirect_uri)

@app.route('/auth/github/callback')
def auth_github_callback():
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    user_info = resp.json()
    frontend_url = "https://visionlangtoolkit.quarry.dpdns.org"
    return redirect(f"{frontend_url}?login=success&username={user_info.get('login')}")

# ==========================================
# EMAIL AUTHENTICATION ROUTES
# ==========================================
@app.route('/signup/email', methods=['POST'])
def signup_email():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    print(f"New User Registered: {email}")
    return jsonify({"status": "success", "message": f"Account created successfully for {email}! (Database pending)"}), 201

@app.route('/login/email', methods=['POST'])
def login_email():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    print(f"User Logged In: {email}")
    return jsonify({"status": "success", "message": f"Welcome back, {email}!"}), 200

# ==========================================
# IMAGE ANALYSIS ROUTE
# ==========================================
@app.route('/analyze', methods=['POST'])
def analyze_api():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400

        file = request.files['image']

        if not file.content_type or not file.content_type.startswith('image/'):
            return jsonify({"error": "Invalid file type. Only images are allowed."}), 400

        filename = secure_filename(file.filename) or "unnamed_image"

        # 1. Calculate File Size
        file.seek(0, os.SEEK_END)
        file_size_bytes = file.tell()
        file.seek(0)
        file_size_kb = round(file_size_bytes / 1024, 2)
        file_size_mb = round(file_size_kb / 1024, 2)
        display_size = f"{file_size_mb} MB" if file_size_mb >= 1 else f"{file_size_kb} KB"

        # 2. Process Image (Supports JPG, PNG, WEBP, GIF, TIFF, BMP, ICO etc.)
        img = Image.open(file.stream)
        width, height = img.size
        img_format = img.format or "Unknown"

        # 3. Advanced Color Space & Depth Detection
        mode = img.mode
        color_space_map = {
            '1': ('Black & White', '1-bit', False),
            'L': ('Grayscale', '8-bit', False),
            'P': ('Paletted', '8-bit', False),
            'RGB': ('RGB (True Color)', '24-bit', False),
            'RGBA': ('RGBA (True Color)', '32-bit', True),
            'CMYK': ('CMYK (Print)', '32-bit', False),
            'YCbCr': ('YCbCr (Video)', '24-bit', False),
            'LAB': ('L*a*b*', '24-bit', False),
            'HSV': ('HSV', '24-bit', False),
            'LA': ('Grayscale + Alpha', '16-bit', True),
            'PA': ('Paletted + Alpha', '16-bit', True)
        }
        
        c_space, c_depth, has_alpha = color_space_map.get(mode, (mode, 'Unknown', False))
        alpha_str = "Yes" if has_alpha else "No"

        # 4. Calculate Aspect Ratio & Orientation
        def get_aspect_ratio(w, h):
            r = math.gcd(w, h)
            return f"{w//r}:{h//r}" if r else "Unknown"

        aspect_ratio = get_aspect_ratio(width, height)
        
        if width > height:
            orientation = "Landscape"
        elif height > width:
            orientation = "Portrait"
        else:
            orientation = "Square"
        
        # 5. Resolution Categorization
        if width >= 3840: resolution_cat = "4K Ultra HD"
        elif width >= 1920: resolution_cat = "Full HD (1080p)"
        elif width >= 1280: resolution_cat = "HD (720p)"
        else: resolution_cat = "Standard Resolution"

        # 6. Extract Dominant Color Palette
        hex_colors = []
        try:
            img.thumbnail((50, 50), resample=Image.Resampling.NEAREST)
            img_rgb = img.convert('RGB')
            palette = img_rgb.quantize(colors=5).getpalette()

            max_len = len(palette) if palette else 0
            for i in range(0, min(15, max_len), 3):
                r, g, b = palette[i], palette[i+1], palette[i+2]
                hex_colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b).upper())

            while len(hex_colors) < 5:
                hex_colors.append('#FFFFFF')
        except Exception as e:
            hex_colors = ["#FFFFFF"] * 5

        attributes = {
            "width": width,
            "height": height,
            "mode": c_space,
            "color_depth": c_depth,
            "has_alpha": alpha_str,
            "format": img_format,
            "orientation": orientation,
            "aspect_ratio": aspect_ratio,
            "filename": filename,
            "file_size": display_size,
            "colors": hex_colors,
            "resolution_category": resolution_cat,
            "timestamp": datetime.now().isoformat()
        }
            
        return jsonify(attributes)
        
    except Exception as e:
        print(f"CRITICAL ERROR: {str(e)}")
        return jsonify({"error": "An internal processing error occurred"}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
        
