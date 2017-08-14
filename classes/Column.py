class Column:

    def __init__(self, name, type, isPrimaryKey):
        self.name = name
        self.type = type
        self.isPrimaryKey = isPrimaryKey
    
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value 

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = value

    @property
    def isPrimaryKey(self):
        return self._isPrimaryKey

    @isPrimaryKey.setter
    def isPrimaryKey(self, value):
        self._isPrimaryKey = value
