import logging
import requests
import sys
from models.currency import currency


def log(func):

    logging.basicConfig(
        level=logging.INFO,
        filename="../logs.log",
        filemode="a",
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s] %(message)s",
    )

    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except requests.exceptions.RequestException:
            logging.error("Ошибка при выполнении запроса к API")
            return None

        except KeyError:
            logging.error("В ответе нет данных о курсах")
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
    result = []

    if "Valute" not in data:
        raise KeyError

    if currency_codes is None:
        currency_codes = list(data["Valute"].keys())

    for code in currency_codes:
        if code in data["Valute"]:
            result.append(
                currency(
                    id=data["Valute"][code]["ID"],
                    num_code=data["Valute"][code]["NumCode"],
                    char_code=data["Valute"][code]["CharCode"],
                    name=data["Valute"][code]["Name"],
                    value=data["Valute"][code]["Value"],
                    nominal=data["Valute"][code]["Nominal"],
                )
            )
        else:
            logging.warning(f"В ответе нет данных о валюте с ключом: {code}")
    return result
