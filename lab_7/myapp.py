from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse


def read_html(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return file.read()


def handle_main():
    html_content = read_html("templates/index.html")
    self.send_response(200)
    self.send_header("Content/type", "text/html")


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        path = parsed_path

        if path == "/":
            self.handle_main()
