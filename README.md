# Real-Time Password Security Lab & Entropy Analyzer 🛡️

A real-time cybersecurity tool designed to analyze password strength, calculate Shannon entropy, and simulate brute-force attacks across various hardware tiers. This project features a unique **mobile-to-dashboard** synchronization using WebSockets and a public reverse proxy tunnel.

## 🚀 Key Features
* **Dual-Interface System:** Scan a QR code to turn any smartphone into a remote input node.
* **Shannon Entropy Engine:** Calculates password complexity in bits to determine true cryptographic strength.
* **Live Dictionary Attack:** Cross-references inputs against a split-part version of the famous `rockyou.txt` (14 million+ passwords).
* **Hardware Simulation:** Provides real-time "Time to Crack" estimates for Mobile devices, High-end GPUs (RTX 4090), and Supercomputers.
* **Global Access:** Integrated with **ngrok** to allow testing from any network (4G/5G/Wi-Fi) without local port forwarding.

---

## 🛠️ Technical Stack
* **Backend:** Python 3.x, Flask
* **Real-Time Sync:** Flask-SocketIO (WebSockets) with Eventlet
* **Frontend:** HTML5, CSS3 (Matrix/Hacker Theme), JavaScript (Vanilla)
* **Tunneling:** Ngrok (Reverse Proxy)
* **Database:** Local flat-file dictionary (Split-part logic)

---

## 📂 Project Structure
```text
├── app.py              # Main Flask server & logic
├── rockyou_part_1.txt  # Split dictionary data (Part 1)
├── rockyou_part_2.txt  # Split dictionary data (Part 2)
├── templates/
│   ├── index.html      # Main Laptop Dashboard
│   └── mobile.html     # Remote Mobile Input Node
└── README.md           # Project documentation
