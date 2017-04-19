import logging
import os
import sqlite3

from . import *
from gpmplgen.db import *
from gpmplgen.gpm.gpmitem import GPMItem


class LibraryDb:
    LIBRARY_DB = 'library'
    GENERATED_PL_DB = 'generated_playlists'

    def __init__(self, db_filename=None):
        self.logger = logging.getLogger(__name__)

        if db_filename is not None:
            db = db_filename
            self.cache_mode = True
            self.logger.debug("Using %s as DB" % db)
        else:
            db = ':memory:'  # In-memory
            self.cache_mode = False
        self.db_conn = sqlite3.connect(db)

    def __del__(self):
        self.db_conn.commit()
        self.db_conn.close()

    def ingest_library(self, gpmLibrary):
        cursor = self.db_conn.cursor()
        try:
            cursor.execute("DROP TABLE %s" % self.LIBRARY_DB)
        except sqlite3.OperationalError:
            pass
        cursor.execute("CREATE TABLE %s %s" % (self.LIBRARY_DB, DbTrack().get_schema()))
        for track in gpmLibrary:
            t = GPMItem(track)
            db_track = DbTrack()
            db_track.from_track(t)
            cursor.execute("INSERT INTO %s VALUES %s" % (self.LIBRARY_DB, db_track.to_sql_placeholder()),
                           db_track.values())
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
            cursor.execute('INSERT INTO %s VALUES %s' % (self.GENERATED_PL_DB, db_playlist.to_sql_placeholder()),
                           db_playlist.values())
        self.db_conn.commit()

    def get_tracks(self, query=''):
        c = self.db_conn.cursor()
        tracks = []
        for row in c.execute("SELECT * FROM %s %s" % (self.LIBRARY_DB, query)):
            db_tracks = DbTrack()
            db_tracks.from_db_row(row)
            tracks.append(db_tracks)
        return tracks

    def get_generated_playlists(self, query=''):
        c = self.db_conn.cursor()
        playlists = []
        for row in c.execute("SELECT * FROM %s %s" % (self.GENERATED_PL_DB, query)):
            db_playlist = DbPlaylist()
            db_playlist.from_db_row(row)
            playlists.append(db_playlist)
        return playlists
