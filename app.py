from flask import Flask, request, render_template_string
from datetime import datetime
import requests
import re

app = Flask(__name__)
LOG_FILE = "logs.txt"

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>IP Logger</title>
    <style>
        body {
            font-family: Arial;
            background: #121212;
            color: #fff;
            text-align: center;
            padding-top: 100px;
        }
        .box {
            border: 1px solid #555;
            padding: 40px;
            margin: auto;
            width: 400px;
            background: #1e1e1e;
            border-radius: 10px;
            box-shadow: 0 0 15px #222;
        }
    </style>
</head>
<body>
    <div class="box">
        <h2>🎯 Your IP has been logged!</h2>
        <p>Thank you for visiting.</p>
    </div>
</body>
</html>
"""

def extract_ipv4(ip):
    if "," in ip:
        ip = ip.split(",")[0]
    match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', ip)
    return match.group(0) if match else ip

@app.route('/')
def index():
    raw_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ip = extract_ipv4(raw_ip)
    ua = request.headers.get('User-Agent')
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        geo = requests.get(f"http://ip-api.com/json/{ip}?fields=country,regionName,city,isp,query").json()
        country = geo.get('country', 'Unknown')
        region = geo.get('regionName', 'Unknown')
        city = geo.get('city', 'Unknown')
        isp = geo.get('isp', 'Unknown')
    except:
        country = region = city = isp = "Error"

    log_entry = f"""
[+] Time       : {time}
[+] IP         : {ip}
[+] Location   : {city}, {region}, {country}
[+] ISP        : {isp}
[+] User-Agent : {ua}
------------------------------
"""
    print(log_entry)
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

    return render_template_string(HTML_PAGE)
