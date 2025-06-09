from flask import Flask, request
import logging

app = Flask(__name__)

# Configure logging to output INFO level logs
logging.basicConfig(level=logging.INFO)

def get_client_ip():
    # Get client IP from X-Forwarded-For header if behind proxy
    if request.headers.getlist("X-Forwarded-For"):
        ip = request.headers.getlist("X-Forwarded-For")[0]
    else:
        ip = request.remote_addr
    return ip

@app.route('/')
def index():
    ip = get_client_ip()
    app.logger.info(f"Visitor IP has been logged! IP: {ip}")
    return f"""
        <h2>Your IP has been logged!</h2>
        <p><strong>IP:</strong> {ip}</p>
    """

if __name__ == "__main__":
    # Run app on all interfaces, port 10000 (or use $PORT env var)
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
