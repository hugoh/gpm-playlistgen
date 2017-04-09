from gmusicapi import Mobileclient
from .library import LibraryDb
import pickle
import sqlite3
import logging
import datetime

class GPMAP:

    def __init__(self, prefix='[GPMAP]', log_level=logging.ERROR, library_cache=None, db_cache=None):
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        self.playlist_prefix = prefix
        self.api = Mobileclient()
        self.cache_file = library_cache
        self.library_db = LibraryDb(db_cache)
        return

    def login(self, username, password):
        self.logger.info('Logging in')
        #return self.api.login(username, password, Mobileclient.FROM_MAC_ADDRESS)

    def _get_all_songs(self):
        save_to_cache = False
        if self.cache_file != None:
            try:
                self.logger.info("Using cache " + self.cache_file)
                library = pickle.load(open(self.cache_file, "rb"))
                self.logger.info("... done")
            except:
                self.logger.error("Reading from cache failed - re-downloading")
        if library == None:
            library = self.api.get_all_songs(incremental=False)
            save_to_cache = True
        if self.cache_file != None and save_to_cache == True:
            self.logger.info("Saving to cache " + self.cache_file)
            pickle.dump(library, open(self.cache_file, "wb"))
        self.logger.info("Loaded %d songs" % (len(library)))
        return library

    def get_library(self):
        if self.library_db.is_initialized():
            return
        library = self._get_all_songs()
        self.library_db.ingest(library)

    def generate_playlist(self, type, config):
        gen_func = getattr(self, type)
        if (gen_func == None):
            self.logger.fatal('Method %s does not exist' % (type))
        gen_func(config)

    def monthly_added(self, config):
        songsByMonth = {}
        for s in self.library_db.get_tracks("ORDER BY creationTimestamp, discNumber, trackNumber"):
            # Group by year & month
            created_time_ms = s.creation_timestamp
            created_time = created_time_ms / (10 ** 6)
            created_yearmonth = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m')
            if songsByMonth.has_key(created_yearmonth) == False:
                songsByMonth[created_yearmonth] = []
            songsByMonth[created_yearmonth].append(s)
        print songsByMonth
