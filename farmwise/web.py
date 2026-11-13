"""Tiny local web chat (standard library only). Run: python -m farmwise serve"""

from __future__ import annotations

import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from . import weather
from .advisor import Advisor

STATIC = Path(__file__).parent / "static"
MAX_BODY = 4096


def make_handler(advisor: Advisor, log_path: Path | None):
    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, payload, content_type="application/json"):
            body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._send(200, (STATIC / "index.html").read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/health":
                self._send(200, {"ok": True, "entries": len(advisor.entries), "kb_status": advisor.meta["status"]})
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            try:
                length = int(self.headers.get("Content-Length", 0))
                if length > MAX_BODY:
                    return self._send(413, {"error": "request too large"})
                data = json.loads(self.rfile.read(length) or b"{}")
            except (ValueError, json.JSONDecodeError):
                return self._send(400, {"error": "invalid JSON"})

            if self.path == "/api/ask":
                question = str(data.get("question", ""))[:500]
                ans = advisor.ask(question)
                text = Advisor.format_sms(ans) if data.get("channel") == "sms" else ans.text
                if log_path:  # question text and outcome only; no user identifiers are stored
                    with log_path.open("a", encoding="utf-8") as f:
                        f.write(json.dumps({"t": int(time.time()), "q": question, "status": ans.status, "docs": ans.doc_ids}) + "\n")
                return self._send(200, {**ans.to_dict(), "text": text})

            if self.path == "/api/weather":
                try:
                    lat, lon = float(data["lat"]), float(data["lon"])
                except (KeyError, TypeError, ValueError):
                    return self._send(400, {"error": "lat and lon are required numbers"})
                rain = weather.fetch_daily_rain(lat, lon)
                if rain is None:
                    return self._send(503, {"error": "forecast unavailable (offline?)"})
                return self._send(200, weather.planting_signal(rain))

            self._send(404, {"error": "not found"})

        def log_message(self, *args):  # keep the console quiet
            pass

    return Handler


def serve(host: str = "127.0.0.1", port: int = 8000, log_path: str | None = "queries.jsonl") -> None:
    advisor = Advisor()
    server = ThreadingHTTPServer((host, port), make_handler(advisor, Path(log_path) if log_path else None))
    print(f"FarmWise running at http://{host}:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
