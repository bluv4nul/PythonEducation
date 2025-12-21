import unittest
import sys
import os

from jinja2 import Environment, PackageLoader, select_autoescape
from pyparsing import Char

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

env = Environment(
    loader=PackageLoader("myapp", "templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

from controllers.authorController import handle_author, handle_home
from controllers.currencyController import handle_currencies
from controllers.userController import handle_users, handle_user_profile


class TestTemplates(unittest.TestCase):
    def test_author(self):
        """Тест шаблона автора"""
        template, context = handle_author()
        self.assertEqual(template, "author.html")
        rendered = env.get_template(template).render(**context)
        self.assertIn('<h1 style="text-align: center;">Страница автора</h1>', rendered)

        template, context = handle_home()
        self.assertEqual(template, "index.html")
        rendered = env.get_template(template).render(**context)
        self.assertIn('<h1 style="text-align: center;">Главная страница</h1>', rendered)

    def test_currencies(self):
        template, context = handle_currencies()

        self.assertEqual(template, "currencies.html")
        self.assertIn("currencies", context)
        rendered = env.get_template(template).render(**context)

        """Таблица есть"""
        self.assertIn("<table", rendered)
        self.assertIn("</table>", rendered)

        """Цикл сработал"""
        self.assertEqual(rendered.count("<tr>"), len(context["currencies"]) + 1)

        """Данные валют отрендерились"""
        currency = context["currencies"][0]
        self.assertIn(currency._char_code, rendered)
        self.assertIn(currency._name, rendered)
        self.assertIn(str(currency._value), rendered)
        self.assertIn(currency._num_code, rendered)

    def test_users(self):
        template, context = handle_users()

        self.assertEqual(template, "users.html")
        self.assertIn("users", context)
        rendered = env.get_template(template).render(**context)

        """Страница отрендерилась"""
        self.assertIn("Список пользователей</h1>", rendered)

        """Список пользователей отрендерился"""
        for user in context["users"]:
            self.assertIn(user._name, rendered)
            self.assertIn(user._id, rendered)

    def test_user_profile(self):
        template, context = handle_user_profile("1")

        self.assertEqual(template, "user.html")
        self.assertIn("user", context)
        self.assertIn("currencies", context)
        rendered = env.get_template(template).render(**context)

        """Страница отрендерилась"""
        self.assertIn("Страница пользователя", rendered)

        """Подписанные валюты отрендерились"""
        for currency in context["currencies"]:
            self.assertIn(currency._char_code, rendered)
            self.assertIn(currency._name, rendered)
            self.assertIn(str(currency._value), rendered)
            self.assertIn(currency._num_code, rendered)


if __name__ == "__main__":
    unittest.main()
