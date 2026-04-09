import math
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO
import eventlet
import glob

# Production-grade networking for WebSockets
eventlet.monkey_patch() 

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

# --- LOGIC FUNCTIONS ---

def check_dictionary(password):
    # This looks for any file starting with 'rockyou_part_'
    parts = glob.glob("rockyou_part_*.txt")
    
    for part_file in parts:
        try:
            with open(part_file, "r", encoding="latin-1") as f:
                for line in f:
                    if line.strip() == password:
                        return True
        except Exception as e:
            print(f"Error reading {part_file}: {e}")
            
    return False

def check_dictionary(password):
    try:
        # Use latin-1 to handle special characters in rockyou.txt
        with open("rockyou.txt", "r", encoding="latin-1") as f:
            for line in f:
                if line.strip() == password:
                    return True
    except FileNotFoundError:
        print("Error: rockyou.txt not found!")
    return False

def calculate_entropy(password):
    if not password:
        return 0, "None"
    
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32 

    entropy = len(password) * math.log2(pool) if pool > 0 else 0
    
    if entropy < 40: strength = "Weak"
    elif entropy < 80: strength = "Medium"
    else: strength = "Strong"
    
    return round(entropy, 2), strength

# --- ROUTES ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/analyze_post', methods=['POST'])
def analyze_post():
    data = request.json
    password = data.get('password', '')
    
    entropy_val, strength_label = calculate_entropy(password)
    leaked = check_dictionary(password)
    
    # Calculate different hardware crack times
    guesses = 2**entropy_val
    times = {
        "Mobile (1M/s)": guesses / 1_000_000,
        "RTX 4090 (50B/s)": guesses / 50_000_000_000,
        "Supercomputer (1T/s)": guesses / 1_000_000_000_000
    }
    
    # Push data to laptop dashboard
    socketio.emit('update_ui', {
        'pass_preview': password[:2] + "*" * (len(password)-2) if len(password) > 2 else password,
        'entropy': entropy_val,
        'strength': strength_label,
        'leaked': leaked,
        'crack_times': times
    })
    
    return jsonify({"status": "success"})

if __name__ == '__main__':
    # host='0.0.0.0' allows external connections via ngrok
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)