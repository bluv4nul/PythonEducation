from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import parse_qs, urlparse

from controllers.authorController import handle_author, handle_home
from controllers.currencyController import handle_currencies
from controllers.userController import handle_users, handle_user_profile


HOST = "localhost"
PORT = 8000


env = Environment(
    loader=PackageLoader("myapp", "templates"), autoescape=select_autoescape()
)


class myHandler(BaseHTTPRequestHandler):

    def render_response(self, template_name, context, status=200):
        if template_name is None:
            self.send_response(status)
            self.send_header("Content-type", "text/plain; charset=utf-8")
            self.end_headers()
            msg = context.get("message", "Error")
            self.wfile.write(bytes(msg.encode("utf-8")))
            return

        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        template = env.get_template(template_name)
        html = template.render(**context)
        self.wfile.write(bytes(html.encode("utf-8")))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)
        user_id = query.get("id", [None])[0]

        try:
            if path == "/":
                template, context = handle_home()
                self.render_response(template, context)

            elif path == "/author":
                template, context = handle_author()
                self.render_response(template, context)

            elif path == "/users":
                template, context = handle_users()
                self.render_response(template, context)

            elif path == "/user":
                result = handle_user_profile(user_id)
                if len(result) == 3:
                    template, context, status = result
                else:
                    template, context = result
                    status = 200
                self.render_response(template, context, status)

            elif path == "/currencies":
                template, context = handle_currencies()
                self.render_response(template, context)

            else:
                self.render_response(None, {"message": "404 Not Found"}, status=404)

        except Exception as e:
            print(f"Error handling request: {e}")
            self.render_response(
                None, {"message": "500 Internal Server Error"}, status=500
            )


if __name__ == "__main__":

    server = HTTPServer((HOST, PORT), myHandler)
    print(f"Starting server at http://{HOST}:{PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()
        print("Server stopped.")
