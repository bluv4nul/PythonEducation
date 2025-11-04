import logging
import requests
import sys

logging.basicConfig(
    level=logging.INFO,
    filename="lab_6/logs.log",
    filemode="w",
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def log(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except requests.exceptions.RequestException:
            logging.error("Ошибка при выполнении запроса к API")
            return None

        except KeyError:
            logging.error("В ответе нет нужной валюты или нет данных о курсах")
            return None

        except ValueError:
            logging.error("Ошибка формата данных (JSON повреждён или пустой)")
            return None

    return wrapper


@log
def get_currencies(
    currency_codes=None, url="https://www.cbr-xml-daily.ru/daily_json.js"
):

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    result = {}

    if currency_codes is None:
        currency_codes = list(data["Valute"].keys())

    if "Valute" not in data:
        raise KeyError

    for code in currency_codes:
        if code in data["Valute"]:
            result[code] = data["Valute"][code]["Value"]
        else:
            logging.warning(f"В ответе нет данных о валюте с ключом: {code}")
    return result
