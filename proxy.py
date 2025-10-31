from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

PORT = 5000
GOOGLE_URL = "https://script.googleusercontent.com/macros/echo?user_content_key=AehSKLgucofFyx5r37GhrWy-_vdqSwC1NovqPWlsd7esq298sCxGha0fmTIM_0e-VMxkQFL79U3JR-CTrvV2_0nh426Sfj94m1PeMNpvxSNT-NEPol8tfdZFesY3FgFCOOP3woDLfHZh3Latf_fACfySGQqVWyxJz5MKbBNwECEGdp_KWolEHk2OKgRFx050ztTNRXTEISGK7CPObRWApCr9ePghyvAqqQWCgyERLxafm-Y2nwUgpNKMdDGwnCY6dA&lib=M8MsR6nk4S0GvFg4g28SDVoOXptZoxvKu"  # <- встав свій Google Web App URL

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            r = requests.post(GOOGLE_URL, headers={"Content-Type": "application/json"}, data=post_data)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')  # CORS
            self.end_headers()
            self.wfile.write(r.content)
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

httpd = HTTPServer(('localhost', PORT), ProxyHandler)
print(f"Проксі-сервер запущено на http://localhost:{PORT}")
httpd.serve_forever()
