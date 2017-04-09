import sqlite3
import os
import logging
from .track import Track

class LibraryDb:
    def __init__(self, db_filename=None):
        self.logger = logging.getLogger(__name__)

        self.initialized = False
        if db_filename != None:
            if os.path.isfile(db_filename):
                self.initialized = True
            db = db_filename
        else:
            db = ':memory:'
        self.logger.debug("Using %s as db (initialized? %s)" % (db, self.initialized))
        self.db_conn = sqlite3.connect(db)

    def __del__(self):
        self.db_conn.close()

    def is_initialized(self):
        return self.initialized

    def ingest(self, library):
        c = self.db_conn.cursor()
        c.execute("CREATE TABLE library %s" % DbTrack.SCHEMA)
        for track in library:
            s = Track(track)
            db_track = DbTrack()
            db_track.from_track(s)
            c.execute("INSERT INTO library %s" % db_track.to_sql())
        self.db_conn.commit()
        self.initialized = True

    def get_tracks(self, query):
        c = self.db_conn.cursor()
        tracks = []
        for row in c.execute("SELECT %s FROM library %s" % (DbTrack.COLUMNS, query)):
            db_tracks = DbTrack()
            db_tracks.from_db_row(row)
            tracks.append(db_tracks)
        return tracks

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
