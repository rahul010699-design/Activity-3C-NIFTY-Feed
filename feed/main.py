import json
import random
import base64
import os
import urllib.request
import urllib.error

from datetime import datetime, time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
SNAPSHOT_FILE = DATA_DIR / "latest_snapshot.json"

ALERTER_URL = os.environ.get(
    "ALERTER_URL",
    "http://127.0.0.1:8001/pubsub"
)


def market_is_open():
    now = datetime.now(IST)
    return (
        now.weekday() < 5
        and time(9, 15) <= now.time() <= time(15, 30)
    )


def generate_snapshot():
    nifty = round(26200 + random.uniform(-100, 100), 2)
    vix = round(14.5 + random.uniform(-1.5, 1.5), 2)

    strikes = [
        round(nifty / 50) * 50 + offset
        for offset in (-100, -50, 0, 50, 100)
    ]

    rows = []
    total_call_oi = 0
    total_put_oi = 0

    for strike in strikes:
        call_oi = random.randint(10000, 100000)
        put_oi = random.randint(10000, 100000)

        total_call_oi += call_oi
        total_put_oi += put_oi

        rows.append({
            "strike": strike,
            "call_oi": call_oi,
            "put_oi": put_oi,
            "call_ltp": round(random.uniform(50, 500), 2),
            "put_ltp": round(random.uniform(50, 500), 2),
        })

    return {
        "timestamp": datetime.now(IST).isoformat(),
        "symbol": "NIFTY",
        "data_mode": "MOCK",
        "market_open": market_is_open(),
        "underlying_price": nifty,
        "india_vix": vix,
        "pcr": round(total_put_oi / total_call_oi, 3),
        "total_call_oi": total_call_oi,
        "total_put_oi": total_put_oi,
        "option_chain": rows,
    }


def save_snapshot(snapshot):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(
        json.dumps(snapshot, indent=2),
        encoding="utf-8",
    )


def publish_snapshot_ready(snapshot):
    event = {
        "event": "snapshot_ready",
        "symbol": snapshot["symbol"],
        "timestamp": snapshot["timestamp"],
    }

    encoded_event = base64.b64encode(
        json.dumps(event).encode("utf-8")
    ).decode("utf-8")

    envelope = {
        "message": {
            "data": encoded_event,
            "messageId": "local-" + str(random.randint(100000, 999999)),
        },
        "subscription": "nifty-alerter-sub",
    }

    request = urllib.request.Request(
        ALERTER_URL,
        data=json.dumps(envelope).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {
                "published": True,
                "alerter_response": result,
            }

    except (urllib.error.URLError, TimeoutError) as error:
        return {
            "published": False,
            "error": str(error),
        }


class FeedHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        body = json.dumps(data, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self.send_json(200, {
                "status": "healthy",
                "service": "nifty-feed",
                "data_mode": "MOCK",
            })

        elif self.path == "/latest":
            if not SNAPSHOT_FILE.exists():
                self.send_json(404, {
                    "error": "No snapshot available. Call POST /collect first."
                })
                return

            snapshot = json.loads(
                SNAPSHOT_FILE.read_text(encoding="utf-8")
            )
            self.send_json(200, snapshot)

        else:
            self.send_json(404, {"error": "Endpoint not found"})

    def do_POST(self):
        if self.path == "/collect":
            snapshot = generate_snapshot()
            save_snapshot(snapshot)

            publish_result = publish_snapshot_ready(snapshot)

            self.send_json(200, {
                "status": "success",
                "message": "Mock NIFTY snapshot collected",
                "snapshot": snapshot,
                "notification": publish_result,
            })

        else:
            self.send_json(404, {"error": "Endpoint not found"})

    def log_message(self, format, *args):
        print(f"[FEED] {self.address_string()} - {format % args}")


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000), FeedHandler)

    print("NIFTY Mock Feed running on port 8000")
    print("Endpoints: GET /health | POST /collect | GET /latest")
    print("Alerter destination:", ALERTER_URL)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping NIFTY Mock Feed...")
        server.server_close()
