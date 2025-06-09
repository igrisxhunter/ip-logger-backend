from flask import Flask, request, render_template_string
import requests
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "logs.txt"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>IP Logger Demo</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #111;
            color: #0f0;
            text-align: center;
            padding-top: 100px;
        }
        .box {
            border: 2px solid #0f0;
            padding: 20px;
            display: inline-block;
        }
    </style>
</head>
<body>
    <div class="box">
        <h1>🎯 Your IP has been logged!</h1>
        <p>This is just a demo logger page.</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        res = requests.get(f"https://ipinfo.io/{ip}/json", timeout=3)
        geo = res.json()
        loc = f"{geo.get('city', '')}, {geo.get('region', '')}, {geo.get('country', '')}"
        org = geo.get("org", "Unknown ISP")
    except Exception:
        loc = "Unknown"
        org = "Unknown"

    log_entry = f"[{now}] IP: {ip} | Location: {loc} | ISP: {org} | Agent: {user_agent}\n"

    print(log_entry.strip())
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    return render_template_string(HTML_PAGE)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Needed for Render
    app.run(host="0.0.0.0", port=port)
