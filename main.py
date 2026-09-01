import os
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify, redirect, session, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit
# সেশন এবং সিকিউরিটির জন্য একটি সিক্রেট কি প্রয়োজন (লগইনের জন্য)
app.secret_key = os.environ.get("SECRET_KEY", "your_super_secret_key_here")

# SECURITY: Restrict CORS to prevent unauthorized cross-origin requests
# আপনার ALLOWED_ORIGINS ভেরিয়েবলে যেন "https://visionlangtoolkit.quarry.dpdns.org" থাকে তা নিশ্চিত করবেন
allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1,https://visionlangtoolkit.quarry.dpdns.org").split(",")
# supports_credentials=True দেওয়া হয়েছে যাতে লগইন সেশন কুকি ঠিকমতো কাজ করে
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

# ==========================================
# OAUTH 2.0 (GOOGLE LOGIN) SETUP
# ==========================================
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.environ.get("GOOGLE_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'},
)

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Online", "message": "API is running!"})

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================
@app.route('/login/google')
def login_google():
    # url_for(...) এর বদলে সরাসরি https লিংকটি লিখে দিন
    redirect_uri = "https://visionlangtoolkit-production.up.railway.app/auth/google/callback"
    return google.authorize_redirect(redirect_uri)
    

@app.route('/auth/google/callback')
def auth_google_callback():
    """গুগল থেকে ভেরিফাই হয়ে ইউজার ডেটা নিয়ে এখানে আসবে"""
    try:
        token = google.authorize_access_token()
        user_info = google.get('userinfo').json()
        
        email = user_info.get('email')
        name = user_info.get('name')
        picture = user_info.get('picture')

        # TODO: এখানে আপনার কাস্টম ডাটাবেজে ইউজার সেভ বা চেক করার লজিক লিখবেন
        
        # সেশনে ইউজারের ইমেইল সেভ করা হলো
        session['user'] = email 

        # সফল হলে ফ্রন্টএন্ডে রিডাইরেক্ট
        frontend_url = "https://visionlangtoolkit.quarry.dpdns.org/?login=success"
        return redirect(frontend_url)
    except Exception as e:
        print(f"OAuth Error: {str(e)}")
        # ফেইল হলে ফ্রন্টএন্ডে এরর প্যারামিটারসহ রিডাইরেক্ট
        return redirect("https://visionlangtoolkit.quarry.dpdns.org/?login=failed")

@app.route('/login/email', methods=['POST'])
def login_email():
    """Email/Password দিয়ে লগইন করার ডামি এন্ডপয়েন্ট"""
    data = request.json
    email = data.get('email')
    password = data.get('password')
    # TODO: ডাটাবেজ চেক
    return jsonify({"message": "Email login endpoint ready", "user": email})

# ==========================================
# IMAGE ANALYSIS ROUTE (ORIGINAL)
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

        # 1. Calculate File Size in KB/MB
        file.seek(0, os.SEEK_END)
        file_size_bytes = file.tell()
        file.seek(0) # Reset pointer to read image
        file_size_kb = round(file_size_bytes / 1024, 2)
        file_size_mb = round(file_size_kb / 1024, 2)
        display_size = f"{file_size_mb} MB" if file_size_mb >= 1 else f"{file_size_kb} KB"

        # 2. Process Image
        img = Image.open(file.stream)
        width, height = img.size
        original_mode = img.mode
        
        # 3. Resolution Categorization
        if width >= 3840: resolution_cat = "4K Ultra HD"
        elif width >= 1920: resolution_cat = "Full HD (1080p)"
        elif width >= 1280: resolution_cat = "HD (720p)"
        else: resolution_cat = "Standard Resolution"

        # 4. Extract Dominant Color Palette (Top 5 Hex Codes)
        hex_colors = []
        try:
            # ⚡ BOLT OPTIMIZATION: Use thumbnail() instead of resize()
            img.thumbnail((50, 50), resample=Image.Resampling.NEAREST)
            img_rgb = img.convert('RGB')
            palette = img_rgb.quantize(colors=5).getpalette()

            # Safely handle palettes shorter than 15 values
            max_len = len(palette) if palette else 0
            for i in range(0, min(15, max_len), 3):
                r, g, b = palette[i], palette[i+1], palette[i+2]
                hex_colors.append('#{:02x}{:02x}{:02x}'.format(r, g, b).upper())

            # Fill missing colors if fewer than 5 were found
            while len(hex_colors) < 5:
                hex_colors.append('#FFFFFF')
        except Exception as e:
            hex_colors = ["#FFFFFF"] * 5 # Fallback

        # Final Response Data
        attributes = {
            "width": width,
            "height": height,
            "mode": original_mode,
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
        
