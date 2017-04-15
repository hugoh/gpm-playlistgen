import time
import logging
import pickle

from gmusicapi import Mobileclient

from .db.library import LibraryDb
from .gpm.playlist import Playlist
from .gpm.playlist_generator import PlaylistGenerator

class GPMAP:

    def __init__(self, username, password, prefix='[GPMAP]', log_level=logging.ERROR, library_cache=None, db_cache=None, dry_run=False):
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        self.playlist_prefix = prefix
        self.client = Mobileclient(debug_logging=False)
        self.logger.info('Logging in %s' % username)
        self.client.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
        if dry_run == True:
            self.writer_client = ClientMock()
        else:
            self.writer_client = self.client
        self.cache_file = library_cache
        self.library_db = LibraryDb(db_cache)
        self.timestamp = time.time()
        self.dry_run = dry_run
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
        # FIXME: also get playlist contents
        library = self._get_all_songs()
        self.library_db.ingest(library)

    def cleanup_previous_playlists(self):
        for pl in self.client.get_all_playlists():
            if not Playlist.is_generated_by_gpmap(pl, self.playlist_prefix):
                self.logger.debug('Skipping %s: %s' % (pl['id'], pl['name']))
                continue
            self.logger.info('Deleting %s: %s' % (pl['id'], pl['name']))
            self.writer_client.delete_playlist(pl['id'])

    def generate_playlist(self, type, config):
        generator = PlaylistGenerator(self.playlist_prefix, self.timestamp, self.library_db)
        try:
            gen_func = getattr(generator, "gen_" + type)
        except AttributeError:
            self.logger.error('Method %s does not exist' % (type))
            return
        playlists = gen_func(config)
        for pl in playlists:
            pl.create_in_gpm(self.writer_client)

class ClientMock():
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def __getattr__(self, name):
        self.logger.info("Not executing %s" % name)
        return self.noop

    def noop(self, *args, **kwargs):
        return