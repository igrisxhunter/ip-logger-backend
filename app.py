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
        app.logger.info(
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
        app.logger.info(
            f"Visitor IP: {ip}\n"
            f"Device Info:\n"
            f"  OS: {os_family} {os_version}\n"
            f"  Browser: {browser_family} {browser_version}\n"
            f"  Device: {device_family}\n"
            f"  Mobile: {is_mobile}, Tablet: {is_tablet}, PC: {is_pc}, Bot: {is_bot}\n"
            f"User-Agent: {user_agent_string}"
        )

    # Build HTML response
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <title>IP & Device Information</title>
      <style>
        body {{
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          background: #eef2f7;
          color: #333;
          margin: 0;
          padding: 2rem;
          display: flex;
          justify-content: center;
          align-items: flex-start;
          min-height: 100vh;
        }}
        .container {{
          background: white;
          padding: 2rem 3rem;
          border-radius: 12px;
          box-shadow: 0 10px 20px rgba(0,0,0,0.1);
          max-width: 480px;
          width: 100%;
        }}
        h1 {{
          color: #2c3e50;
          margin-bottom: 1rem;
          text-align: center;
        }}
        .section {{
          margin-bottom: 1.5rem;
        }}
        .section h2 {{
          margin-bottom: 0.5rem;
          color: #2980b9;
          border-bottom: 2px solid #2980b9;
          padding-bottom: 0.25rem;
          font-size: 1.2rem;
        }}
        .info p {{
          margin: 0.2rem 0;
          line-height: 1.4;
          word-wrap: break-word;
        }}
        .label {{
          font-weight: 600;
          color: #555;
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <h1>Your IP and Device Info</h1>

        <div class="section">
          <h2>IP & Location</h2>
          <div class="info">
            <p><span class="label">IP:</span> {info['IP'] if info else ip}</p>
            <p><span class="label">Country:</span> {info['Country'] if info else 'N/A'}</p>
            <p><span class="label">Region:</span> {info['Region'] if info else 'N/A'}</p>
            <p><span class="label">City:</span> {info['City'] if info else 'N/A'}</p>
            <p><span class="label">ISP:</span> {info['ISP'] if info else 'N/A'}</p>
            <p><span class="label">Timezone:</span> {info['Timezone'] if info else 'N/A'}</p>
            <p><span class="label">Coordinates:</span> {info['Lat'] if info else 'N/A'}, {info['Lon'] if info else 'N/A'}</p>
          </div>
        </div>

        <div class="section">
          <h2>Device Info</h2>
          <div class="info">
            <p><span class="label">Operating System:</span> {os_family} {os_version}</p>
            <p><span class="label">Browser:</span> {browser_family} {browser_version}</p>
            <p><span class="label">Device:</span> {device_family}</p>
            <p><span class="label">Mobile:</span> {is_mobile}</p>
            <p><span class="label">Tablet:</span> {is_tablet}</p>
            <p><span class="label">PC:</span> {is_pc}</p>
            <p><span class="label">Bot:</span> {is_bot}</p>
            <p><span class="label">User-Agent:</span> <small>{user_agent_string}</small></p>
          </div>
        </div>
      </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
