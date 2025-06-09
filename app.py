import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

@app.route("/")
def home():
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    # Use only IPv4, if IPv6, get first IPv4 from ipinfo API or fallback
    ip = ip.split(',')[0].strip()

    # Get geolocation info from ipinfo.io
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()
    city = data.get('city', 'Unknown City')
    region = data.get('region', 'Unknown Region')
    country = data.get('country', 'Unknown Country')
    org = data.get('org', 'Unknown Org')

    # Save log
    with open('logs.txt', 'a') as f:
        f.write(f"IP: {ip} | Location: {city}, {region}, {country} | ISP: {org}\n")

    # Simple page
    return render_template_string(f"""
        <h2>Your IP has been logged!</h2>
        <p><strong>IP:</strong> {ip}</p>
        <p><strong>Location:</strong> {city}, {region}, {country}</p>
        <p><strong>ISP:</strong> {org}</p>
    """)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use PORT from Render or default 5000
    app.run(host="0.0.0.0", port=port)
