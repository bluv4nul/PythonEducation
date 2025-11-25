from http.server import HTTPServer, BaseHTTPRequestHandler
from models import *
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import parse_qs
import os
import mimetypes

HOST = "localhost"
PORT = 8000

env = Environment(
    loader=PackageLoader("myapp", "templates"), autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")
template_user = env.get_template("user.html")


class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        if self.path.startswith("/static/"):
            static_root = os.path.normpath(
                os.path.join(os.path.dirname(__file__), "static")
            )
            rel = self.path[len("/static/") :]
            full_path = os.path.normpath(os.path.join(static_root, rel))
            if not full_path.startswith(static_root) or not os.path.exists(full_path):
                self.send_response(404)
                self.end_headers()
                return
            ctype, _ = mimetypes.guess_type(full_path)
            self.send_response(200)
            if ctype:
                self.send_header("Content-Type", ctype)
            self.end_headers()
            with open(full_path, "rb") as f:
                self.wfile.write(f.read())

        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_index.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/users":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_users.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/user":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_user.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/currencies":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_currencies.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/author":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_author.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))


server = HTTPServer((HOST, PORT), myHandler)

try:
    print("Server now running ...")
    server.serve_forever()
except KeyboardInterrupt:
    print("Received interrupt, stopping server...")
finally:
    server.shutdown()
    server.server_close()
    print("Server closed ...")
