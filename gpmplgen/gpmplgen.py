import time
import logging
import pickle

from gmusicapi import Mobileclient

from clientmock import ClientMock
from .db.library import LibraryDb
from gpm import *


class GPMPlGen:

    def __init__(self, config):
        self.config = config
        
        logging.basicConfig(level=config.log_level)
        self.logger = logging.getLogger(__name__)

        # Client
        self.client = Mobileclient(debug_logging=False)
        gmusicapi_logger = logging.getLogger('gmusicapi.utils')
        gmusicapi_logger.setLevel(logging.INFO)

        # Logging in
        self.logger.info('Logging in %s' % config.username)
        try:
            self.client.login(config.username, config.password, Mobileclient.FROM_MAC_ADDRESS)
        except Exception as e:
            raise GPMPlGenException("Could not log in", e)

        # Setting up writer
        if config.dry_run:
            self.logger.info('Running in DRY-RUN mode; setting up mock client...')
            self.writer_client = ClientMock()
        else:
            self.writer_client = self.client

        # Local store
        self.library_db = LibraryDb(config.db_cache)

        # Internal stuff
        self.timestamp = time.time()

    def _get_all_songs(self):
        # FIXME: this is ugly; separate cache stuff out
        save_to_cache = False
        library_from_gpm = None
        if self.config.library_cache is not None:
            try:
                self.logger.debug("Using cache " + self.config.library_cache)
                library_from_gpm = pickle.load(open(self.config.library_cache, "rb"))
                self.logger.debug("... done")
            except pickle.PickleError:
                self.logger.warn("Reading from cache failed - re-downloading")
        if library_from_gpm is None:
            self.logger.info("Downloading all tracks from library")
            try:
                library_from_gpm = self.client.get_all_songs(incremental=False)
            except Exception as e:
                GPMPlGenException("Could not download library", e)
            save_to_cache = True
        if self.config.library_cache is not None and save_to_cache:
            self.logger.debug("Saving to cache " + self.config.library_cache)
            pickle.dump(library_from_gpm, open(self.config.library_cache, "wb"))
        self.logger.info("Loaded %d songs" % (len(library_from_gpm)))
        return library_from_gpm

    def get_library(self, get_songs=True, get_playlists=True):
        if self.library_db.is_initialized():
            return

        # Get songs
        if get_songs:
            library_from_gpm = self._get_all_songs()
            self.library_db.ingest_library(library_from_gpm)
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
        playlists_from_gpm = []
        try:
            playlists_from_gpm = self.client.get_all_playlists()
        except Exception as e:
            GPMPlGenException("Could not download playlists", e)
        generated_playlists = []
        for pl in playlists_from_gpm:
            if not Playlist.is_generated_by_gpmplgen(pl):
                self.logger.debug('Skipping %s: %s' % (pl['id'], pl['name']))
                continue
            generated_playlists.append(pl)
        return generated_playlists

    def delete_playlists(self, playlists):
        # FIXME: replace with playlist.delete
        for pl in playlists:
            self.logger.info('Deleting %s: %s' % (pl.id, pl.name))
            self.writer_client.delete_playlist(pl.id)

    def cleanup_all_generated_playlists(self):
        self.delete_playlists(self.library_db.get_generated_playlists())

    def generate_playlist(self, playlist_type, config):
        generator = PlaylistGenerator(self.config.playlist_prefix, self.timestamp, self.library_db)
        try:
            generator_results = generator.generate(playlist_type, config)
        except AttributeError:
            self.logger.error('Method %s does not exist' % playlist_type)
            return
        self.delete_playlists(generator_results.get_playlists_to_delete())
        playlists_to_create = generator_results.get_playlists_to_create()
        try:
            for pl in playlists_to_create:
                pl.create_in_gpm(self.writer_client)
        except GPMPlGenException as e:
            self.logger.error("Error talking to Google Play Music; attempting to clean-up")
            for pl in playlists_to_create:
                pl.delete_in_gpm(self.writer_client)
            self.logger.debug(e.parent_exception)
            raise e  # FIXME: maybe not?


class GPMPlGenException(Exception):
    def __init__(self, message, parent_exception):
        self.message = message
        self.parent_exception = parent_exception

    def __str__(self):
        logging.getLogger(__name__).debug(self.parent_exception)
        return self.message
