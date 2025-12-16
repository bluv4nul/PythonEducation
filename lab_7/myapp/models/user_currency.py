from models import user


class UserCurrency:
    def __init__(self, user: user.User, currency_id: list = None):
        self._id = id(self)
        self._user_id = user.id
        self._currency_id = currency_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id

    @property
    def currency_id(self):
        return self._currency_id

    @currency_id.setter
    def currency_id(self, currency_id):
        self._currency_id = currency_id
