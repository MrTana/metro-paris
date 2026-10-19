#!/usr/bin/env python3
"""Servidor local para la pantalla de metro de París.

Sirve metro-paris.html y reenvía /api/... a la API de PRIM (evita el bloqueo CORS
del navegador). La clave API la envía la propia página en la cabecera "apikey".

Uso:   python servidor.py            ->  abre http://localhost:8765
       python servidor.py 9000       ->  otro puerto
"""
import http.server, json, os, sys, urllib.request, urllib.error

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8765
HERE = os.path.dirname(os.path.abspath(__file__))
UPSTREAM = "https://prim.iledefrance-mobilites.fr/marketplace/v2/navitia/coverage/fr-idf"


class Handler(http.server.BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(os.path.join(HERE, "metro-paris.html"), "rb") as f:
                return self._send(200, f.read(), "text/html; charset=utf-8")
        if self.path == "/api/ping":
            return self._send(200, json.dumps({"ok": True}).encode())
        if self.path.startswith("/api/"):
            req = urllib.request.Request(UPSTREAM + self.path[4:])
            key = self.headers.get("apikey")
            if key:
                req.add_header("apikey", key)
            try:
                with urllib.request.urlopen(req, timeout=20) as r:
                    return self._send(r.status, r.read())
            except urllib.error.HTTPError as e:
                return self._send(e.code, e.read() or b"{}")
            except Exception as e:  # red caída, DNS, etc.
                return self._send(502, json.dumps({"error": str(e)}).encode())
        self._send(404, b"{}")

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    print(f"Pantalla de metro en http://localhost:{PORT}  (Ctrl+C para salir)")
    http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
