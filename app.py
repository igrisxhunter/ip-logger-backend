from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Simple IP Logger</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
        .card { background-color: #f2f2f2; padding: 20px; border-radius: 8px; display: inline-block; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #333; }
        p { margin: 5px 0; font-size: 18px; }
        .tag { font-size: 12px; color: #777; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="card">
        <h1>🎯 IP Logger</h1>
        <p><strong>Your IP:</strong> {{ ip }}</p>
        <p><strong>Location:</strong> {{ city }}, {{ region }}, {{ country }}</p>
        <p><strong>ISP:</strong> {{ isp }}</p>
        <div class="tag">Tool: subfinder</div>
    </div>
</body>
</html>
"""

def get_client_ip(req):
    return req.headers.get("X-Forwarded-For", req.remote_addr).split(',')[0].strip()

def fetch_ip_details(ip):
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json", timeout=5)
        data = res.json()
        return {
            "ip": ip,
            "city": data.get("city", "Unknown"),
            "region": data.get("region", "Unknown"),
            "country": data.get("country_name", "Unknown"),
            "isp": data.get("org", "Unknown")
        }
    except Exception as e:
        return {
            "ip": ip,
            "city": "Error",
            "region": "Error",
            "country": "Error",
            "isp": "Error"
        }

@app.route('/')
def index():
    ip = get_client_ip(request)
    info = fetch_ip_details(ip)

    # Log to Render console
    print(f"[IP LOGGER] IP: {info['ip']} | Location: {info['city']}, {info['region']}, {info['country']} | ISP: {info['isp']}")

    return render_template_string(HTML_TEMPLATE, **info)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
