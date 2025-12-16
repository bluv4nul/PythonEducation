from http.server import HTTPServer, BaseHTTPRequestHandler
from jinja2 import Environment, PackageLoader, select_autoescape
from utils.currencies_api import get_currencies
from models import user, user_currency
from urllib.parse import parse_qs, urlparse

env = Environment(
    loader=PackageLoader("myapp", "templates"), autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_currencies = env.get_template("currencies.html")
template_author = env.get_template("author.html")
template_user = env.get_template("user.html")

HOST = "localhost"
PORT = 8000

Users = [
    user.User(1, "Petya"),
    user.User(2, "Vanya"),
    user.User(3, "Fedya"),
    user.User(4, "Max"),
]

UserCurrency = [
    user_currency.UserCurrency(Users[0], ["R01090B", "R01105", "R01200"]),
    user_currency.UserCurrency(Users[1], ["R01230", "R01215", "R01239"]),
    user_currency.UserCurrency(Users[2], ["R01280", "R01300", "R01350"]),
    user_currency.UserCurrency(Users[3]),
]

currencies_data = get_currencies()


class myHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        query = parse_qs(parsed.query)

        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_index.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif path == "/currencies":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_currencies.render(currencies=currencies_data)

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif path == "/users":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_users.render(users=Users)

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif path == "/user":

            user_id = query.get("id", [""])[0]

            try:
                uid = int(user_id)
            except ValueError:
                uid = None

            user = next((u for u in Users if getattr(u, "_id", None) == uid))
            if user == None:
                self.send_response(200)
                self.send_header("Content-type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(b"User not found")

            subscribed_curr_id = None
            for uc in UserCurrency:
                if getattr(uc, "_user_id", None) == getattr(user, "_id", None):
                    subscribed_curr_id = getattr(uc, "_currency_id", None)
                    break

            subscribed_currencies = []
            if subscribed_curr_id:
                for cid in subscribed_curr_id:
                    for currency in currencies_data:
                        cur_id = getattr(currency, "_id", None)
                        if cid == cur_id:
                            subscribed_currencies.append(currency)
                            break

            html_content = template_user.render(
                user=user, currencies=(subscribed_currencies or [])
            )

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            self.wfile.write(bytes(html_content.encode("utf-8")))


server = HTTPServer((HOST, PORT), myHandler)

try:
    print("Server now running ...")
    print("Adress http://localhost:8000")
    server.serve_forever()
except KeyboardInterrupt:
    server.server_close()
    print("Received interrupt, stopping server...")
