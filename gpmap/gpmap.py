import time
import datetime
import logging
import pickle

from gmusicapi import Mobileclient

from .db.library import LibraryDb
from .gpm.playlist import Playlist


class GPMAP:

    def __init__(self, username, password, prefix='[GPMAP]', log_level=logging.ERROR, library_cache=None, db_cache=None):
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        self.playlist_prefix = prefix
        self.client = Mobileclient(debug_logging=False)
        self.logger.info('Logging in %s' % username)
        self.client.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
        self.cache_file = library_cache
        self.library_db = LibraryDb(db_cache)
        self.timestamp = time.time()
        return

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
            library = self.client.get_all_songs(incremental=False)
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

    def cleanup_previous_playlists(self):
        for pl in self.client.get_all_playlists():
            if pl['name'].startswith(self.playlist_prefix):
                self.logger.info('Deleting %s: %s' % (pl['id'], pl['name']))
                self.client.delete_playlist(pl['id'])

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
                songsByMonth[created_yearmonth] = Playlist(self.playlist_prefix + ' Added in ' + created_yearmonth)
            songsByMonth[created_yearmonth].add_track(s.id)
        for m in sorted(songsByMonth.keys()):
            pl = songsByMonth[m]
            for p in pl.get_ingestable_playlists():
                self.logger.info("Creating playlist " + p.get_name())
                playlist_id = self.client.create_playlist(p.get_name(), description=p.get_description())
                self.client.add_songs_to_playlist(playlist_id, p.tracks)
