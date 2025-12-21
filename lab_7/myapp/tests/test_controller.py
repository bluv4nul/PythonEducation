import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from controllers.userController import *
from controllers.currencyController import *
from controllers.authorController import *


class TestControllers(unittest.TestCase):

    def test_user_controller(self):
        """Тесты контроллера пользователей"""

        """handle_users"""
        template, context = handle_users()
        self.assertEqual(template, "users.html")
        self.assertIn("users", context)
        self.assertEqual(len(context["users"]), 4)

        """user_id = None"""
        template, context, status = handle_user_profile(None)
        self.assertIsNone(template)
        self.assertEqual(status, 400)
        self.assertIn("message", context)

        """user not found"""
        template, context, status = handle_user_profile("999")
        self.assertIsNone(template)
        self.assertEqual(status, 404)
        self.assertIn("message", context)

        """valid user_id"""
        template, context = handle_user_profile("1")
        self.assertEqual(template, "user.html")
        self.assertIn("user", context)
        self.assertIn("currencies", context)
        self.assertEqual(context["user"]._name, "Petya")

    def test_currency_controller(self):
        """Тесты контроллера валют"""
        template, context = handle_currencies()
        self.assertEqual(template, "currencies.html")
        self.assertIn("currencies", context)
        self.assertGreater(len(context["currencies"]), 0)

    def test_author_controller(self):
        """Тесты контроллера автора"""
        template, context = handle_author()
        self.assertEqual(template, "author.html")

        template, context = handle_home()
        self.assertEqual(template, "index.html")


if __name__ == "__main__":
    unittest.main()
