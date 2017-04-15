import string

class DbItem:

    def __init__(self, columns):
        self._columns = columns

    def get_columns(self):
        names = map(lambda c: c.get_name(), self._columns)
        return string.join(names, ',')

    def get_schema(self):
        definition = map(lambda c: c.get_column_def(), self._columns)
        return '(' + string.join(definition, ',') + ')'

    def from_db_row(self, row):
        i = 0
        for c in self._columns:
            a = c.get_name()
            setattr(self, a, row[i])

class DbColumn:
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def get_name(self):
        return self.name

    def get_column_def(self):
        return '%s %s' % (self.name, string.upper(self.type))