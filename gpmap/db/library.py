import logging
import os
import sqlite3

from gpmap.gpm.gpmitem import GPMItem
from dbtrack import DbTrack
from dbplaylist import DbPlaylist

class LibraryDb:
    LIBRARY_DB = 'library'
    GENERATED_PL_DB = 'generated_playlists'

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
        cursor = self.db_conn.cursor()
        cursor.execute("CREATE TABLE %s %s" % (self.LIBRARY_DB, DbTrack().get_schema()))
        for track in library:
            t = GPMItem(track)
            db_track = DbTrack()
            db_track.from_track(t)
            cursor.execute("INSERT INTO %s VALUES %s" % (self.LIBRARY_DB, db_track.to_sql_placeholder()), db_track.values())
        self.db_conn.commit()
        self.initialized = True

    def ingest_generated_playlists(self, playlists):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("DROP TABLE %s" % self.GENERATED_PL_DB)
        except sqlite3.OperationalError:
            pass
        cursor.execute("CREATE TABLE %s %s" % (self.GENERATED_PL_DB, DbPlaylist().get_schema()))
        for pl in playlists:
            p = GPMItem(pl)
            db_playlist = DbPlaylist()
            db_playlist.from_playlist(p)
            cursor.execute('INSERT INTO %s VALUES %s' % (self.GENERATED_PL_DB, db_playlist.to_sql_placeholder()), db_playlist.values())
        self.db_conn.commit()

    def get_tracks(self, query = ''):
        c = self.db_conn.cursor()
        tracks = []
        for row in c.execute("SELECT * FROM %s %s" % (self.LIBRARY_DB, query)):
            db_tracks = DbTrack()
            db_tracks.from_db_row(row)
            tracks.append(db_tracks)
        return tracks

    def get_generated_playlists(self, query = ''):
        c = self.db_conn.cursor()
        playlists = []
        for row in c.execute("SELECT * FROM %s %s" % (self.GENERATED_PL_DB, query)):
            db_playlist = DbPlaylist()
            db_playlist.from_db_row(row)
            playlists.append(db_playlist)
        return playlists

