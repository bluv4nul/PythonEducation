class User:
    def __init__(self, id: str, name: str):
        if not isinstance(id, str) or not isinstance(name, str):
            raise TypeError()

        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, id):
        self._id = id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
