class app:
    def __init__(self, name, version, author):
        self._name = name
        self._version = version
        self._author = author

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, version):
        self._version = version

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, author):
        self._author = author
