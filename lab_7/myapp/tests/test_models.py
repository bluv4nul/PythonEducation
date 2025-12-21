import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from models.app import *
from models.author import *
from models.currency import *
from models.user import *
from models.user_currency import *


class TestModels(unittest.TestCase):

    def tests_creation(self):
        """Тесты создания моделей"""
        app = App("MyApp", "1.0", "Andrew")
        author = Author("Andrew", "ИВТ-2")
        currency = Currency("R10101", "123", "USD", "Доллар США", 52, 1)
        user = User("id", "Name")
        user_currency = UserCurrency(user, ["12345"])
        self.assertEqual(app._name, "MyApp")
        self.assertEqual(app._version, "1.0")
        self.assertEqual(app._author, "Andrew")

        self.assertEqual(author._name, "Andrew")
        self.assertEqual(author._group, "ИВТ-2")

        self.assertEqual(currency._id, "R10101")
        self.assertEqual(currency._num_code, "123")
        self.assertEqual(currency._char_code, "USD")
        self.assertEqual(currency._name, "Доллар США")
        self.assertEqual(currency._value, 52)
        self.assertEqual(currency._nominal, 1)

        self.assertEqual(user._id, "id")
        self.assertEqual(user._name, "Name")

        self.assertEqual(user_currency._user_id, user._id)
        self.assertEqual(user_currency._currency_id, ["12345"])

    def tests_getters_setters(self):
        """Тесты геттеров и сеттеров моделей"""
        app = App("MyApp", "1.0", "Andrew")
        author = Author("Andrew", "ИВТ-2")
        currency = Currency("R10101", "123", "USD", "Доллар США", 52, 1)
        user = User("id", "Name")
        user_currency = UserCurrency(user, ["12345"])

        self.assertEqual(app._name, "MyApp")
        app._name = "NewName"
        self.assertEqual(app._name, "NewName")

        self.assertEqual(author._name, "Andrew")
        author._name = "NewAuthor"
        self.assertEqual(author._name, "NewAuthor")

        self.assertEqual(currency._name, "Доллар США")
        currency._name = "Евро"
        self.assertEqual(currency._name, "Евро")

        self.assertEqual(user._name, "Name")
        user._name = "NewUser"
        self.assertEqual(user._name, "NewUser")

        self.assertEqual(user_currency._currency_id, ["12345"])
        user_currency._currency_id = ["NewCurrencyID"]
        self.assertEqual(user_currency._currency_id, ["NewCurrencyID"])

    def test_types(self):
        """Ошибки типов App"""
        with self.assertRaises(TypeError):
            App(123, "1.0", "Andrew")
        with self.assertRaises(TypeError):
            App("MyApp", 1.0, "Andrew")
        with self.assertRaises(TypeError):
            App("MyApp", "1.0", 456)

        """Ошибки типов Author"""
        with self.assertRaises(TypeError):
            Author(123, "ИВТ-2")
        with self.assertRaises(TypeError):
            Author("Andrew", 456)

        """Ошибки типов Currency"""
        with self.assertRaises(TypeError):
            Currency(10101, "123", "USD", "Доллар США", 52, 1)
        with self.assertRaises(TypeError):
            Currency("R10101", 123, "USD", "Доллар США", 52, 1)
        with self.assertRaises(TypeError):
            Currency("R10101", "123", 456, "Доллар США", 52, 1)
        with self.assertRaises(TypeError):
            Currency("R10101", "123", "USD", 789, 52, 1)
        with self.assertRaises(TypeError):
            Currency("R10101", "123", "USD", "Доллар США", "52", 1)
        with self.assertRaises(TypeError):
            Currency("R10101", "123", "USD", "Доллар США", 52, "1")

        """Ошибки типов User"""
        with self.assertRaises(TypeError):
            User(123, "Name")
        with self.assertRaises(TypeError):
            User("id", 456)

        """Ошибки типов UserCurrency"""
        with self.assertRaises(TypeError):
            UserCurrency(123, ["R10101"])
        with self.assertRaises(TypeError):
            UserCurrency(User("id", "Name"), 12345)


if __name__ == "__main__":
    unittest.main()
