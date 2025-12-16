class Author:
    def __init__(self, name, group):
        self._name = name
        self._group = group

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def group(self):
        return self._group

    @group.setter
    def group(self, group):
        self._group = group
