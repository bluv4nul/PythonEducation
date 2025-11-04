import unittest
from unittest.mock import patch, MagicMock
import logging
import os
import requests

from get_currencies import get_currencies


class TestGetCurrencies(unittest.TestCase):
    def setUp(self):
        """Подготовка перед каждым тестом"""
        # Удаляем старый лог-файл, если есть
        if os.path.exists("lab_6/logs.log"):
            open("lab_6/logs.log", "w", encoding="utf-8").close()

    # ---------- 1. Проверка корректного результата ----------
    @patch("get_currencies.requests.get")
    def test_valid_response(self, mock_get):
        """Проверяем, что функция возвращает правильные ключи и значения"""
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "Valute": {"USD": {"Value": 90.5}, "EUR": {"Value": 95.3}}
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "EUR"])

        self.assertIsInstance(result, dict)
        self.assertIn("USD", result)
        self.assertIn("EUR", result)
        self.assertEqual(result["USD"], 90.5)
        self.assertEqual(result["EUR"], 95.3)

    # ---------- 2. Проверка обработки ошибок ----------
    @patch("get_currencies.requests.get")
    def test_api_exception(self, mock_get):
        """Проверяем, что RequestException обрабатывается корректно"""
        mock_get.side_effect = requests.exceptions.RequestException("Ошибка API")
        result = get_currencies(["USD"])
        self.assertIsNone(result)

    # ---------- 3. Проверка логирования ----------
    @patch("get_currencies.requests.get")
    def test_warning_logged_for_missing_currency(self, mock_get):
        """Проверяем, что отсутствующая валюта записывается в лог"""
        mock_response = MagicMock()
        mock_response.json.return_value = {"Valute": {"USD": {"Value": 90.0}}}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        result = get_currencies(["USD", "ABC"])
        self.assertIn("USD", result)
        self.assertNotIn("ABC", result)

        # Проверяем, что лог действительно содержит предупреждение
        with open("lab_6/logs.log", "r", encoding="utf-8") as f:
            log_text = f.read()
        self.assertIn("В ответе нет данных о валюте с ключом: ABC", log_text)


if __name__ == "__main__":
    unittest.main()
