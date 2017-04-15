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
        DbItem.__init__(self, columns)

    def from_track(self, track):
        self.id = track.get('id')
        self.album_id = track.get('albumId', '')
        self.disc_number = int(track.get('discNumber', 0))
        self.track_number = int(track.get('trackNumber', 0))
        self.creation_timestamp = int(track.get('creationTimestamp', 0))
        self.play_count = int(track.get('playCount', 0))
