
import base64
import json
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
SNAPSHOT_FILE = DATA_DIR / "latest_snapshot.json"
PREVIOUS_FILE = DATA_DIR / "previous_snapshot.json"
ALERT_LOG = DATA_DIR / "alerts.log"

PCR_LOW = 0.70
PCR_HIGH = 1.30
VIX_JUMP_PCT = 10.0


def read_snapshot():
    if not SNAPSHOT_FILE.exists():
        raise FileNotFoundError("No snapshot found. Collect feed data first.")

    return json.loads(SNAPSHOT_FILE.read_text(encoding="utf-8"))


def evaluate_alerts(snapshot):
    alerts = []

    pcr = float(snapshot["pcr"])
    vix = float(snapshot["india_vix"])

    if pcr < PCR_LOW:
        alerts.append({
            "type": "PCR_LOW",
            "message": f"PCR is below threshold: {pcr}"
        })

    if pcr > PCR_HIGH:
        alerts.append({
            "type": "PCR_HIGH",
            "message": f"PCR is above threshold: {pcr}"
        })

    if PREVIOUS_FILE.exists():
        previous = json.loads(
            PREVIOUS_FILE.read_text(encoding="utf-8")
        )
        previous_vix = float(previous["india_vix"])

        if previous_vix > 0:
            jump = ((vix - previous_vix) / previous_vix) * 100

            if jump >= VIX_JUMP_PCT:
                alerts.append({
                    "type": "VIX_JUMP",
                    "message": f"India VIX increased by {jump:.2f}%"
                })

    PREVIOUS_FILE.write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8"
    )

    return alerts


def save_alerts(alerts, snapshot):
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    with ALERT_LOG.open("a", encoding="utf-8") as file:
        for alert in alerts:
            event = {
                "timestamp": datetime.now().astimezone().isoformat(),
                "symbol": snapshot.get("symbol", "NIFTY"),
                "data_mode": snapshot.get("data_mode", "MOCK"),
                **alert
            }
            file.write(json.dumps(event) + "\n")


class AlerterHandler(BaseHTTPRequestHandler):

    def send_json(self, status, payload):
        body = json.dumps(payload, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {
                "status": "healthy",
                "service": "nifty-alerter"
            })
        else:
            self.send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path != "/pubsub":
            self.send_json(404, {"error": "Endpoint not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            request_body = self.rfile.read(length)
            envelope = json.loads(request_body)

            message = envelope.get("message", {})
            encoded_data = message.get("data")

            if not encoded_data:
                self.send_json(400, {
                    "error": "Missing Pub/Sub message data"
                })
                return

            decoded = base64.b64decode(encoded_data)
            event = json.loads(decoded)

            snapshot = read_snapshot()
            alerts = evaluate_alerts(snapshot)
            save_alerts(alerts, snapshot)

            self.send_json(200, {
                "status": "processed",
                "event": event,
                "alert_count": len(alerts),
                "alerts": alerts
            })

        except Exception as error:
            self.send_json(500, {
                "status": "error",
                "message": str(error)
            })

    def log_message(self, format, *args):
        print(f"[ALERTER] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8001), AlerterHandler)
    print("NIFTY Alerter running at http://127.0.0.1:8001")
    print("Endpoints: GET /health | POST /pubsub")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping NIFTY Alerter...")
        server.server_close()

