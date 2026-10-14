"""Tiny JSON API + static file server built only on the standard library."""

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from exceptions import (DuplicateStudentError, StudentError,
                        StudentNotFoundError)
from manager import StudentManager

STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
LOCK = threading.Lock()
MANAGER = None


class Handler(BaseHTTPRequestHandler):
    # --- helpers -------------------------------------------------------
    def _send(self, status, payload, content_type="application/json"):
        body = payload if isinstance(payload, bytes) else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        length = int(self.headers.get("Content-Length") or 0)
        try:
            return json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            raise StudentError("Request body is not valid JSON.")

    def _student_id(self, path):
        parts = path.strip("/").split("/")
        return parts[2] if len(parts) == 3 else None

    def _handle(self, fn):
        try:
            with LOCK:
                status, data = fn()
            self._send(status, data)
        except StudentNotFoundError as exc:
            self._send(404, {"error": str(exc)})
        except DuplicateStudentError as exc:
            self._send(409, {"error": str(exc)})
        except StudentError as exc:
            self._send(400, {"error": str(exc)})
        except Exception as exc:  # last-resort guard so the server never dies
            self._send(500, {"error": f"Server error: {exc}"})

    # --- routes --------------------------------------------------------
    def do_GET(self):
        url = urlparse(self.path)
        if url.path == "/api/students":
            q = parse_qs(url.query).get("q", [""])[0]
            return self._handle(lambda: (200, [
                s.to_dict() for s in (MANAGER.search(q) if q else MANAGER.all())]))
        if url.path == "/api/stats":
            return self._handle(lambda: (200, MANAGER.stats()))
        self._static(url.path)

    def do_POST(self):
        url = urlparse(self.path)
        if url.path == "/api/students":
            def create():
                d = self._body()
                s = MANAGER.add(d.get("student_id", ""), d.get("name", ""),
                                d.get("age"), d.get("course", ""), d.get("marks", {}))
                return 201, s.to_dict()
            return self._handle(create)
        if url.path == "/api/seed":
            def seed():
                count = int(parse_qs(url.query).get("count", ["5"])[0])
                return 201, {"added": MANAGER.seed(max(1, min(count, 50)))}
            return self._handle(seed)
        self._send(404, {"error": "Not found"})

    def do_PUT(self):
        sid = self._student_id(urlparse(self.path).path)
        if not sid:
            return self._send(404, {"error": "Not found"})

        def update():
            d = self._body()
            s = MANAGER.update(sid, d.get("name", ""), d.get("age"),
                               d.get("course", ""), d.get("marks"))
            return 200, s.to_dict()
        self._handle(update)

    def do_DELETE(self):
        sid = self._student_id(urlparse(self.path).path)
        if not sid:
            return self._send(404, {"error": "Not found"})
        self._handle(lambda: (200, MANAGER.delete(sid).to_dict()))

    # --- static files --------------------------------------------------
    def _static(self, path):
        rel = "index.html" if path in ("", "/") else path.lstrip("/")
        full = os.path.normpath(os.path.join(STATIC_DIR, rel))
        if not full.startswith(STATIC_DIR) or not os.path.isfile(full):
            return self._send(404, {"error": "Not found"})
        ctype = {".html": "text/html", ".js": "text/javascript",
                 ".css": "text/css"}.get(os.path.splitext(full)[1], "application/octet-stream")
        with open(full, "rb") as fh:
            self._send(200, fh.read(), ctype + "; charset=utf-8")

    def log_message(self, fmt, *args):
        print(f"[HTTP] {self.address_string()} {fmt % args}")


def run(host="127.0.0.1", port=8000):
    global MANAGER
    MANAGER = StudentManager()
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"Student Management System running at http://{host}:{port}  (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        server.server_close()
