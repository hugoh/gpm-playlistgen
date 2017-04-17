import time
import logging
import pickle

from gmusicapi import Mobileclient

from clientmock import ClientMock
from .db.library import LibraryDb
from .gpm.playlist import Playlist
from .gpm.playlist_generator import PlaylistGenerator


class GPMPlGen:

    DEFAULT_PREFIX='[PG]'

    def __init__(self, username, password, prefix=DEFAULT_PREFIX, log_level=logging.ERROR, library_cache=None, db_cache=None,
                 force=False, dry_run=False):
        logging.basicConfig(level=log_level)
        self.logger = logging.getLogger(__name__)

        # Client
        self.client = Mobileclient(debug_logging=False)
        self.logger.info('Logging in %s' % username)
        self.client.login(username, password, Mobileclient.FROM_MAC_ADDRESS)
        if dry_run == True:
            self.writer_client = ClientMock()
        else:
            self.writer_client = self.client

        self.playlist_prefix = prefix

        # Local store
        self.cache_file = library_cache
        self.library_db = LibraryDb(db_cache)

        # Internal stuff
        self.timestamp = time.time()
        self.force = force
        self.dry_run = dry_run

    def _get_all_songs(self):
        save_to_cache = False
        library = None
        if self.cache_file != None:
            try:
                self.logger.debug("Using cache " + self.cache_file)
                library = pickle.load(open(self.cache_file, "rb"))
                self.logger.debug("... done")
            except:
                self.logger.warn("Reading from cache failed - re-downloading")
        if library == None:
            self.logger.info("Downloading all tracks from library")
            library = self.client.get_all_songs(incremental=False)
            save_to_cache = True
        if self.cache_file != None and save_to_cache == True:
            self.logger.debug("Saving to cache " + self.cache_file)
            pickle.dump(library, open(self.cache_file, "wb"))
        self.logger.info("Loaded %d songs" % (len(library)))
        return library

    def get_library(self, get_songs=True, get_playlists=True):
        if self.library_db.is_initialized():
            return

        # Get songs
        if get_songs:
            library = self._get_all_songs()
            self.library_db.ingest_library(library)
        else:
            self.logger.info('Skipping getting songs')

        # Get generated playlists
        if get_playlists:
            playlists = self._get_all_generated_playlists()
            self.library_db.ingest_generated_playlists(playlists)
        else:
            self.logger.info('Skipping getting playlists')
            # FIXME: also get playlist contents?

    def _get_all_generated_playlists(self):
        self.logger.info('Getting playlists')
        playlists = []
        for pl in self.client.get_all_playlists():
            if not Playlist.is_generated_by_gpmplgen(pl):
                self.logger.debug('Skipping %s: %s' % (pl['id'], pl['name']))
                continue
            playlists.append(pl)
        return playlists

    def delete_playlists(self, playlists):
        for pl in playlists:
            self.logger.info('Deleting %s: %s' % (pl.id, pl.name))
            self.writer_client.delete_playlist(pl.id)

    def cleanup_all_generated_playlists(self):
        self.delete_playlists(self.library_db.get_generated_playlists())

    def generate_playlist(self, type, config):
        generator = PlaylistGenerator(self.playlist_prefix, self.timestamp, self.library_db)
        try:
            generator_results = generator.generate(type, config)
        except AttributeError:
            self.logger.error('Method %s does not exist' % (type))
            return
        self.delete_playlists(generator_results.delete_playlists)
        for pl in generator_results.new_playlists:
            pl.create_in_gpm(self.writer_client)
