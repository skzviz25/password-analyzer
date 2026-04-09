import math
import hashlib
import requests
import re
import glob
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- SECURITY LOGIC ---

def check_local_dictionary(password):
    """Checks the split rockyou parts on the laptop."""
    target = password.strip()
    parts = glob.glob("rockyou_part_*.txt")
    for part in parts:
        try:
            with open(part, "r", encoding="latin-1") as f:
                for line in f:
                    if line.strip() == target:
                        return True
        except: continue
    return False

def check_hibp_api(password):
    """Checks the global database using k-Anonymity (SHA-1 prefix)."""
    sha1_pw = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_pw[:5], sha1_pw[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url, timeout=3)
        if res.status_code == 200:
            return any(line.split(':')[0] == suffix for line in res.text.splitlines())
    except: return False
    return False

def get_insights(password):
    """Pattern recognition for common password habits."""
    hints = []
    if len(password) < 8: hints.append("Length below industry standard")
    if re.search(r'(.)\1{2,}', password): hints.append("Repeating characters detected")
    if any(s in password.lower() for s in ["123", "abc", "qwerty", "asdf"]): hints.append("Keyboard sequence detected")
    return hints if hints else ["Complexity patterns look unique"]

def calculate_entropy(password):
    if not password: return 0, "None"
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32
    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    strength = "Weak" if entropy < 40 else "Medium" if entropy < 80 else "Strong"
    return round(entropy, 2), strength

# --- ROUTES ---

@app.route('/')
def index(): return render_template('index.html')

@app.route('/mobile')
def mobile(): return render_template('mobile.html')

@app.route('/analyze_post', methods=['POST'])
def analyze_post():
    data = request.json
    password = data.get('password', '')
    
    entropy_val, strength_label = calculate_entropy(password)
    local_leaked = check_local_dictionary(password)
    api_leaked = check_hibp_api(password)
    insights = get_insights(password)
    
    guesses = 2**entropy_val
    times = {
        "Old Desktop (10k/s)": guesses / 10_000,
        "RTX 4090 GPU (50B/s)": guesses / 50_000_000_000,
        "Cloud Cluster (1T/s)": guesses / 1_000_000_000_000
    }
    
    socketio.emit('update_ui', {
        'entropy': entropy_val,
        'strength': strength_label,
        'local': local_leaked,
        'api': api_leaked,
        'insights': insights,
        'times': times
    })
    return jsonify({"status": "received"})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)