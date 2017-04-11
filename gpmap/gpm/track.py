class Track:

    def __init__(self, track):
        self.track = track

    def get(self, field):
        return self.track[field]

    def get_string_value(self, field):
        if self.track.has_key(field):
            return self.track[field]
        else:
            return ''

    def get_int_value(self, field):
        if self.track.has_key(field):
            return int(self.track[field])
        else:
            return 0