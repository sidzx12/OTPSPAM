#!/usr/bin/env python3
"""Mock OTP endpoint dengan rate limiting. Bind localhost saja."""
import json, time, threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BIND = ("127.0.0.1", 8765)

WINDOW_SEC   = 60     # jendela observasi
MAX_PER_WIN  = 3      # maks OTP per nomor per jendela
COOLDOWN_SEC = 30     # jeda antar request sukses

_state = {}            # phone -> {"hits": [...], "last": ts}
_lock  = threading.Lock()

def check(phone: str):
    now = time.time()
    with _lock:
        s = _state.setdefault(phone, {"hits": [], "last": 0.0})
        s["hits"] = [t for t in s["hits"] if now - t < WINDOW_SEC]
        if now - s["last"] < COOLDOWN_SEC:
            return 429, {"error": "cooldown", "retry_after": int(COOLDOWN_SEC - (now - s["last"]))}
        if len(s["hits"]) >= MAX_PER_WIN:
            return 429, {"error": "window_exceeded", "retry_after": WINDOW_SEC}
        s["hits"].append(now)
        s["last"] = now
        return 200, {"status": "otp_sent", "phone_tail": phone[-4:]}

class H(BaseHTTPRequestHandler):
    def _send(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        if self.path != "/api/otp/request":
            return self._send(404, {"error": "not_found"})
        try:
            n = int(self.headers.get("Content-Length", 0))
            data = json.loads(self.rfile.read(n) or b"{}")
        except Exception:
            return self._send(400, {"error": "bad_json"})
        phone = str(data.get("phone", ""))
        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            return self._send(400, {"error": "bad_phone"})
        code, payload = check(phone)
        self._send(code, payload)

    def log_message(self, fmt, *args):
        pass  # log via demo, bukan stderr server

if __name__ == "__main__":
    srv = ThreadingHTTPServer(BIND, H)
    print(f"[lab] listening on http://{BIND[0]}:{BIND[1]}")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.server_close()
