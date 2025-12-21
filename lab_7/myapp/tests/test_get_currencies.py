import unittest
import sys
import os
import requests
from unittest.mock import patch, Mock


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.currencies_api import get_currencies


class TestCurrenciesAPI(unittest.TestCase):
    def test_get_currencies(self):
        """Тест получения данных о валютах"""
        currencies = get_currencies()
        self.assertIsInstance(currencies, list)
        self.assertGreater(len(currencies), 0)
        for currency in currencies:
            self.assertTrue(hasattr(currency, "_id"))
            self.assertTrue(hasattr(currency, "_num_code"))
            self.assertTrue(hasattr(currency, "_char_code"))
            self.assertTrue(hasattr(currency, "_name"))
            self.assertTrue(hasattr(currency, "_value"))
            self.assertTrue(hasattr(currency, "_nominal"))

    @patch("utils.currencies_api.requests.get")
    def test_network_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException
        self.assertIsNone(get_currencies())

    @patch("utils.currencies_api.requests.get")
    def test_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.side_effect = ValueError
        mock_get.return_value = mock_response

        self.assertIsNone(get_currencies())

    @patch("utils.currencies_api.requests.get")
    def test_no_valute_key(self, mock_get):
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.json.return_value = {"Date": "2025-01-01"}
        mock_get.return_value = mock_response

        self.assertIsNone(get_currencies())


if __name__ == "__main__":
    unittest.main()
