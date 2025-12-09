from http.server import HTTPServer, BaseHTTPRequestHandler
from models import *
from jinja2 import Environment, PackageLoader, select_autoescape
from urllib.parse import parse_qs
from utils.currencies_api import get_currencies
import os
import mimetypes
import json
import logging
import sqlite3
import threading
import time
import datetime

users_db = sqlite3.connect("./myapp/database/USERS_DATA.db")
users_currencies_db = sqlite3.connect("./myapp/database/USERS_CURRENCIES.db")

CURRENCIES_DB_PATH = os.path.join(
    os.path.dirname(__file__), "database", "CURRENCIES_DATA.db"
)
DB_LOCK = threading.Lock()

USERS_DB_PATH = os.path.join(os.path.dirname(__file__), "database", "USERS_DATA.db")
USERS_CURRENCIES_DB_PATH = os.path.join(
    os.path.dirname(__file__), "database", "USERS_CURRENCIES.db"
)


def ensure_user_tables():
    try:
        conn = sqlite3.connect(USERS_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()
        conn.close()

        conn = sqlite3.connect(USERS_CURRENCIES_DB_PATH)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                currency_char_code TEXT NOT NULL,
                created_at TEXT,
                UNIQUE(user_id, currency_char_code)
            )
            """
        )
        conn.commit()
        conn.close()
    except Exception:
        logging.exception("Ошибка при создании таблиц пользователей/подписок")


def fetch_and_cache(interval_sec: int = 60):
    while True:
        try:
            currencies = get_currencies()
            if currencies:
                with DB_LOCK:
                    conn = sqlite3.connect(CURRENCIES_DB_PATH, timeout=10)
                    cur = conn.cursor()
                    cur.execute(
                        """
                        CREATE TABLE IF NOT EXISTS currencies (
                            char_code TEXT PRIMARY KEY,
                            id TEXT,
                            num_code INTEGER,
                            name TEXT,
                            value REAL,
                            nominal INTEGER,
                            updated_at TEXT
                        )
                        """
                    )
                    now = datetime.datetime.utcnow().isoformat()
                    for c in currencies:
                        # c — объект currency с атрибутами: id, num_code, char_code, name, value, nominal
                        cur.execute(
                            """
                            INSERT OR REPLACE INTO currencies
                            (char_code, id, num_code, name, value, nominal, updated_at)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            """,
                            (
                                getattr(c, "char_code", ""),
                                getattr(c, "id", ""),
                                getattr(c, "num_code", None),
                                getattr(c, "name", ""),
                                getattr(c, "value", 0.0),
                                getattr(c, "nominal", None),
                                now,
                            ),
                        )
                    conn.commit()
                    conn.close()
        except Exception:
            logging.exception("Ошибка при обновлении кеша валют в БД")
        time.sleep(interval_sec)


ensure_user_tables()
threading.Thread(target=fetch_and_cache, args=(60,), daemon=True).start()

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

        elif self.path.startswith("/users") and self.command == "GET":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # list users and provide form to create new user
            users = []
            try:
                conn = sqlite3.connect(USERS_DB_PATH)
                cur = conn.cursor()
                cur.execute("SELECT id, name FROM users ORDER BY id DESC")
                rows = cur.fetchall()
                for r in rows:
                    users.append({"id": r[0], "name": r[1]})
                conn.close()
            except Exception:
                logging.exception("Ошибка чтения списка пользователей")

            html_content = template_users.render(users=users)

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path.startswith("/user") and self.command == "GET":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            user_id = None
            try:
                if "?" in self.path:
                    qs = self.path.split("?", 1)[1]
                    params = parse_qs(qs)
                    user_id = params.get("id", [None])[0]
            except Exception:
                logging.exception("Ошибка парсинга параметров запроса /user")

            user_obj = None
            try:
                if user_id:
                    conn = sqlite3.connect(USERS_DB_PATH)
                    cur = conn.cursor()
                    cur.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
                    row = cur.fetchone()
                    conn.close()
                    if row:
                        user_obj = {"id": row[0], "name": row[1]}
            except Exception:
                logging.exception("Ошибка чтения пользователя")

            currencies_data = []
            try:
                with DB_LOCK:
                    if os.path.exists(CURRENCIES_DB_PATH):
                        conn = sqlite3.connect(CURRENCIES_DB_PATH)
                        cur = conn.cursor()
                        cur.execute(
                            "SELECT id, num_code, char_code, name, value, nominal FROM currencies"
                        )
                        rows = cur.fetchall()
                        for r in rows:
                            currencies_data.append(
                                {
                                    "_id": r[0],
                                    "_num_code": r[1],
                                    "_char_code": r[2],
                                    "_name": r[3],
                                    "_value": r[4],
                                    "_nominal": r[5],
                                }
                            )
                        conn.close()
            except Exception:
                logging.exception("Ошибка чтения валют из БД")

            subscribed_codes = []
            try:
                if user_obj:
                    conn = sqlite3.connect(USERS_CURRENCIES_DB_PATH)
                    cur = conn.cursor()
                    cur.execute(
                        "SELECT currency_char_code FROM subscriptions WHERE user_id = ?",
                        (user_obj["id"],),
                    )
                    rows = cur.fetchall()
                    subscribed_codes = [r[0] for r in rows]
                    conn.close()
            except Exception:
                logging.exception("Ошибка чтения подписок пользователя")

            html_content = template_user.render(
                user=user_obj,
                currencies=currencies_data,
                subscribed_codes=subscribed_codes,
            )

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/currencies":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            currencies_data = []

            try:
                with DB_LOCK:
                    if os.path.exists(CURRENCIES_DB_PATH):
                        conn = sqlite3.connect(CURRENCIES_DB_PATH)
                        cur = conn.cursor()
                        cur.execute(
                            "SELECT id, num_code, char_code, name, value, nominal FROM currencies"
                        )
                        rows = cur.fetchall()
                        for r in rows:
                            currencies_data.append(
                                {
                                    "_id": r[0],
                                    "_num_code": r[1],
                                    "_char_code": r[2],
                                    "_name": r[3],
                                    "_value": r[4],
                                    "_nominal": r[5],
                                }
                            )
                        conn.close()
            except Exception:
                logging.exception("Ошибка чтения валют из БД")

            html_content = template_currencies.render().replace(
                "//CURRENCIES_DATA;",
                f"const currenciesData = {json.dumps(currencies_data)};",
            )

            self.wfile.write(bytes(html_content.encode("utf-8")))

        elif self.path == "/author":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = template_author.render()

            self.wfile.write(bytes(html_content.encode("utf-8")))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        params = parse_qs(body)

        if self.path == "/create_user":
            name = params.get("name", [""])[0].strip()
            if name:
                try:
                    conn = sqlite3.connect(USERS_DB_PATH)
                    cur = conn.cursor()
                    cur.execute("INSERT INTO users (name) VALUES (?)", (name,))
                    conn.commit()
                    user_id = cur.lastrowid
                    conn.close()
                    self.send_response(303)
                    self.send_header("Location", f"/user?id={user_id}")
                    self.end_headers()
                    return
                except Exception:
                    logging.exception("Ошибка создания пользователя")
            self.send_response(400)
            self.end_headers()
            return

        if self.path == "/subscribe":
            user_id = params.get("user_id", [""])[0]
            currency_list = params.get("currency", [])
            if not user_id:
                self.send_response(400)
                self.end_headers()
                return
            try:
                conn = sqlite3.connect(USERS_CURRENCIES_DB_PATH)
                cur = conn.cursor()
                cur.execute("DELETE FROM subscriptions WHERE user_id = ?", (user_id,))
                now = datetime.datetime.utcnow().isoformat()
                for code in currency_list:
                    cur.execute(
                        "INSERT OR IGNORE INTO subscriptions (user_id, currency_char_code, created_at) VALUES (?, ?, ?)",
                        (user_id, code, now),
                    )
                conn.commit()
                conn.close()
            except Exception:
                logging.exception("Ошибка обновления подписок")
            self.send_response(303)
            self.send_header("Location", f"/user?id={user_id}")
            self.end_headers()
            return

        self.send_response(404)
        self.end_headers()


server = HTTPServer((HOST, PORT), myHandler)

try:
    print("Server now running ...")
    print("Adress http://localhost:8000")
    server.serve_forever()
except KeyboardInterrupt:
    print("Received interrupt, stopping server...")
finally:
    server.shutdown()
    server.server_close()
    print("Server closed ...")
