from utils.currencies_api import get_currencies


def handle_currencies():
    currencies_data = get_currencies()
    return "currencies.html", {"currencies": currencies_data}
