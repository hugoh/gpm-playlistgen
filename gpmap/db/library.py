import logging
import os
import sqlite3

from gpmap.gpm.gpmitem import GPMItem
from .dbtrack import DbTrack

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

    def ingest_library(self, library):
        c = self.db_conn.cursor()
        c.execute("CREATE TABLE library %s" % DbTrack().get_schema())
        for track in library:
            t = GPMItem(track)
            db_track = DbTrack()
            db_track.from_track(t)
            c.execute("INSERT INTO library %s" % db_track.to_sql())
        self.db_conn.commit()
        self.initialized = True

    def ingest_generated_playlists(self, playlists):
        c = self.db_conn.cursor()
        c.execute("DROP TABLE generated_playlists")
        c.execute("CREATE TABLE generated_playlists (id, name, description)")
        for pl in playlists:
            gpm_playlist = GPMItem(pl)
            c.execute('INSERT INTO generated_playlists ("%s", "%s", "%s")' %
                      (gpm_playlist.get('id'), gpm_playlist.get('name'), gpm_playlist.get_string_value('description')))

    def get_tracks(self, query):
        c = self.db_conn.cursor()
        tracks = []
        for row in c.execute("SELECT %s FROM library %s" % (DbTrack().get_columns(), query)):
            db_tracks = DbTrack()
            db_tracks.from_db_row(row)
            tracks.append(db_tracks)
        return tracks
