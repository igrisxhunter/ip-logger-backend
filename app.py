from flask import Flask, request
import requests
import logging
from user_agents import parse

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

def get_client_ip():
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0].split(',')[0].strip()
    else:
        ip = request.remote_addr
    return ip

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                return {
                    "IP": ip,
                    "Country": data.get('country', 'N/A'),
                    "Region": data.get('regionName', 'N/A'),
                    "City": data.get('city', 'N/A'),
                    "ISP": data.get('isp', 'N/A'),
                    "Timezone": data.get('timezone', 'N/A'),
                    "Lat": data.get('lat', 'N/A'),
                    "Lon": data.get('lon', 'N/A'),
                }
    except Exception as e:
        app.logger.error(f"Failed to fetch IP info: {e}")
    return None

@app.route('/')
def index():
    ip = get_client_ip()
    info = get_ip_info(ip)

    user_agent_string = request.headers.get('User-Agent', 'Unknown')
    user_agent = parse(user_agent_string)

    os_family = user_agent.os.family
    os_version = user_agent.os.version_string
    browser_family = user_agent.browser.family
    browser_version = user_agent.browser.version_string
    device_family = user_agent.device.family
    is_mobile = user_agent.is_mobile
    is_tablet = user_agent.is_tablet
    is_pc = user_agent.is_pc
    is_bot = user_agent.is_bot

    if info:
        log_msg = (
            f"Visitor IP: {info['IP']}\n"
            f"Location: {info['City']}, {info['Region']}, {info['Country']}\n"
            f"ISP: {info['ISP']}\n"
            f"Timezone: {info['Timezone']}\n"
            f"Coordinates: {info['Lat']}, {info['Lon']}\n"
            f"Device Info:\n"
            f"  OS: {os_family} {os_version}\n"
            f"  Browser: {browser_family} {browser_version}\n"
            f"  Device: {device_family}\n"
            f"  Mobile: {is_mobile}, Tablet: {is_tablet}, PC: {is_pc}, Bot: {is_bot}\n"
            f"User-Agent: {user_agent_string}"
        )
    else:
        log_msg = (
            f"Visitor IP: {ip}\n"
            f"Device Info:\n"
            f"  OS: {os_family} {os_version}\n"
            f"  Browser: {browser_family} {browser_version}\n"
            f"  Device: {device_family}\n"
            f"  Mobile: {is_mobile}, Tablet: {is_tablet}, PC: {is_pc}, Bot: {is_bot}\n"
            f"User-Agent: {user_agent_string}"
        )

    app.logger.info(log_msg)

    # Hacker style HTML page output
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>Access Denied</title>
      <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        body {{
          background-color: #0f0f0f;
          color: #00ff00;
          font-family: 'Share Tech Mono', monospace;
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100vh;
          margin: 0;
          text-shadow: 0 0 5px #00ff00;
        }}
        h1 {{
          font-size: 3rem;
          margin-bottom: 0.5rem;
        }}
        p {{
          font-size: 1.5rem;
          margin-top: 0;
        }}
        .emoji {{
          font-size: 3rem;
          margin-top: 1rem;
          animation: flicker 1.5s infinite;
        }}
        @keyframes flicker {{
          0%, 100% {{ opacity: 1; }}
          50% {{ opacity: 0.6; }}
        }}
      </style>
    </head>
    <body>
      <h1>🚨 ACCESS DENIED 🚨</h1>
      <p>Your IP <strong>{ip}</strong> and device info have been logged.</p>
      <div class="emoji">👾💀🔒</div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
