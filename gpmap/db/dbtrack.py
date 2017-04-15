from dbitem import *

class DbTrack(DbItem):

    def __init__(self):
        columns = [
            DbColumn('id', 'TEXT'),
            DbColumn('albumId', 'TEXT'),
            DbColumn('discNumber', 'INTEGER'),
            DbColumn('trackNumber', 'INTEGER'),
            DbColumn('creationTimestamp', 'INTEGER'),
            DbColumn('playCount', 'INTEGER')
        ]
        DbItem.__init__(columns)

    def from_track(self, track):
        self.id = track.get('id')
        self.album_id = track.get_string_value('albumId')
        self.disc_number = track.get_int_value('discNumber')
        self.track_number = track.get_int_value('trackNumber')
        self.creation_timestamp = track.get_int_value('creationTimestamp')
        self.play_count = track.get_int_value('playCount')

    def to_sql(self):
        return "(%s) VALUES ('%s', '%s', %d, %d, %d, %d)"\
               % (self.get_columns(), self.id, self.album_id, self.disc_number, self.track_number, self.creation_timestamp, self.play_count)
