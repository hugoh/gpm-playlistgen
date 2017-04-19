import yaml
import logging


class Config:
    DEFAULT_PREFIX = '[PG]'

    def __init__(self):
        self.username = None
        self.password = None
        self.playlist_prefix = self.DEFAULT_PREFIX
        self.log_level = logging.INFO
        self.library_cache = None
        self.db_cache = None
        self.force = False
        self.dry_run = False
        self.delete_all_playlists = False
        self.playlists = []

    def fromYaml(self, path):
        cfg = yaml.load(path)
        self.username = cfg['auth']['user']
        self.password = cfg['auth']['passwd']
        self.playlist_prefix = cfg['prefix']
        self.playlists = cfg['playlists']
        self.library_cache = Config._get_cache_path(cfg, 'libraryCache')
        self.db_cache = Config._get_cache_path(cfg, 'dbFile')
        try:
            if cfg['dev']['debug']:
                self.log_level = logging.DEBUG
        except KeyError:
            pass

    def fromCli(self, args):
        self.force = args.force
        self.dry_run = args.dry_run
        self.delete_all_playlists = args.delete_all_playlists

    @staticmethod
    def _get_cache_path(cfg, cache_type):
        try:
            return cfg['dev'][cache_type]
        except KeyError:
            return None
