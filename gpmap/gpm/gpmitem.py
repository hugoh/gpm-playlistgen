class GPMItem:

    def __init__(self, item):
        self.item = item

    def get(self, field):
        return self.item[field]

    def get_string_value(self, field):
        if self.item.has_key(field):
            return self.item[field]
        else:
            return ''

    def get_int_value(self, field):
        if self.item.has_key(field):
            return int(self.item[field])
        else:
            return 0