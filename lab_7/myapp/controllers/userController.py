from models import user, user_currency
from utils.currencies_api import get_currencies

Users = [
    user.User("1", "Petya"),
    user.User("2", "Vanya"),
    user.User("3", "Fedya"),
    user.User("4", "Max"),
]

UserCurrency = [
    user_currency.UserCurrency(Users[0], ["R01090B", "R01105", "R01200"]),
    user_currency.UserCurrency(Users[1], ["R01230", "R01215", "R01239"]),
    user_currency.UserCurrency(Users[2], ["R01280", "R01300", "R01350"]),
    user_currency.UserCurrency(Users[3]),
]

currencies_data = get_currencies()


def get_currencies_data():
    return currencies_data


def handle_users():
    return "users.html", {"users": Users}


def handle_user_profile(user_id):
    if user_id is None:
        return None, {"message": "User ID not provided."}, 400

    user_obj = next((u for u in Users if u._id == user_id), None)
    if user_obj is None:
        return None, {"message": "User not found."}, 404

    subscribed_curr_id = None
    for uc in UserCurrency:
        if uc._user_id == user_obj._id:
            subscribed_curr_id = uc._currency_id
            break

    subscribed_currencies = []
    if subscribed_curr_id:
        for cid in subscribed_curr_id:
            for currency in currencies_data:
                if getattr(currency, "_id", None) == cid:
                    subscribed_currencies.append(currency)
                    break

    return (
        "user.html",
        {"user": user_obj, "currencies": subscribed_currencies},
    )
