import os
from datetime import datetime
from PIL import Image
from flask import Flask, request, jsonify, redirect, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix 
from authlib.integrations.flask_client import OAuth # NEW: Authlib ইমপোর্ট

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
app.secret_key = os.environ.get("SECRET_KEY", "your_super_secret_key_here")

allowed_origins = os.environ.get("ALLOWED_ORIGINS", "http://localhost,http://127.0.0.1,https://visionlangtoolkit.quarry.dpdns.org").split(",")
CORS(app, resources={r"/*": {"origins": allowed_origins}}, supports_credentials=True)

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
    """গিটহাব লগইন পেজে রিডাইরেক্ট করবে"""
    redirect_uri = "https://visionlangtoolkit-production.up.railway.app/auth/github/callback"
    return github.authorize_redirect(redirect_uri)

@app.route('/auth/github/callback')
def auth_github_callback():
    """গিটহাব থেকে ভেরিফাই হয়ে ডেটা নিয়ে আসার রাউট"""
    token = github.authorize_access_token()
    resp = github.get('user', token=token)
    user_info = resp.json()
    
    # লগইন সফল হলে আপনার ফ্রন্টএন্ড ওয়েবসাইটে রিডাইরেক্ট করে দেবে
    frontend_url = "https://visionlangtoolkit.quarry.dpdns.org"
    return redirect(f"{frontend_url}?login=success&username={user_info.get('login')}")

# ==========================================
# IMAGE ANALYSIS ROUTE (আপনার আগের কোড)
# ==========================================
@app.route('/analyze', methods=['POST'])
def analyze_api():
# ... (আপনার analyze ফাংশনের ভেতরের বাকি কোড যেমন ছিল তেমনই থাকবে) ...
