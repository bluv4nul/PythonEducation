class currency:
    def __init__(self, id, num_code, char_code, name, value, nominal):
        self._id = id
        self._num_code = num_code
        self._char_code = char_code
        self._name = name
        self._value = value
        self._nominal = nominal

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def num_code(self):
        return self._num_code

    @num_code.setter
    def num_code(self, num_code):
        self._num_code = num_code

    @property
    def char_code(self):
        return self._char_code

    @char_code.setter
    def char_code(self, char_code):
        self._char_code = char_code

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, nominal):
        self._nominal = nominal
