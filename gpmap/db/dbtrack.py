class DbTrack:
    # FIXME: less hard-coding

    SCHEMA = '(id TEXT, albumId TEXT, discNumber INTEGER, trackNumber INTEGER, creationTimestamp INTEGER, playCount INTEGER)'
    COLUMNS = 'id, albumId, discNumber, trackNumber, creationTimestamp, playCount'

    def from_track(self, track):
        self.id = track.get('id')
        self.album_id = track.get_string_value('albumId')
        self.disc_number = track.get_int_value('discNumber')
        self.track_number = track.get_int_value('trackNumber')
        self.creation_timestamp = track.get_int_value('creationTimestamp')
        self.play_count = track.get_int_value('playCount')

    def from_db_row(self, row):
        self.id = row[0]
        self.album_id = row[1]
        self.disc_number = row[2]
        self.track_number = row[3]
        self.creation_timestamp = row[4]
        self.play_count = row[5]


    def to_sql(self):
        return "(%s) VALUES ('%s', '%s', %d, %d, %d, %d)"\
               % (DbTrack.COLUMNS, self.id, self.album_id, self.disc_number, self.track_number, self.creation_timestamp, self.play_count)
