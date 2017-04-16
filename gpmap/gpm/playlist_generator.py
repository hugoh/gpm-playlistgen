import datetime
import logging

from .playlist import Playlist
from gpmap.db.dbplaylist import DbPlaylistCache

class PlaylistGeneratorResults():
    def __init__(self, delete_playlists, new_playlists):
        self.delete_playlists = delete_playlists
        self.new_playlists = new_playlists

class PlaylistGenerator():
    MONTHLY_ADDED = 'monthly_added'
    MOST_PLAYED = 'most_played'

    def __init__(self, playlist_prefix, timestamp, library_db):
        self.logger = logging.getLogger(__name__)
        self.playlist_prefix = playlist_prefix
        self.timestamp = timestamp
        self.library_db = library_db

    def generate(self, playlist_type, config):
        gen_func = getattr(self, "_gen_" + playlist_type)
        return gen_func(config)

    def full_playlist_name(self, name):
        if self.playlist_prefix != None and len(self.playlist_prefix) > 0:
            return self.playlist_prefix + ' ' + name
        else:
            return name

    @staticmethod
    def _gen_yearmonth(timestamp):
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m')

    @staticmethod
    def _is_yearmonth_old(current, tested):
        return tested < current

    def _gen_monthly_added(self, config):
        songs_by_month = {}
        current_yearmonth = self._gen_yearmonth(self.timestamp)
        dbplaylist_cache = DbPlaylistCache()
        delete_playlists = []
        new_playlists = []
        for track in self.library_db.get_tracks("ORDER BY creationTimestamp, discNumber, trackNumber"):
            # Group by year & month
            created_time_ms = track.creationTimestamp
            created_time = created_time_ms / (10 ** 6)
            created_yearmonth = self._gen_yearmonth(created_time)
            pl_type = self.MONTHLY_ADDED
            pl_args = created_yearmonth
            current_playlists_final = dbplaylist_cache.are_final_check(pl_type, pl_args)
            if current_playlists_final == None:
                existing_playlists = self.library_db.get_generated_playlists("WHERE type='%s' AND args='%s'" % (pl_type, pl_args))
                current_playlists_final = dbplaylist_cache.are_final(pl_type, pl_args, existing_playlists)
                if current_playlists_final == False:
                    delete_playlists += existing_playlists
                else:
                    self.logger.info('Skipping %s:%s' % (pl_type, pl_args))
            if current_playlists_final == True:
                continue
            if songs_by_month.has_key(created_yearmonth) == False:
                pl = Playlist(self.full_playlist_name('Added in ' + created_yearmonth), self.timestamp)
                pl.set_type(pl_type)
                pl.set_args(pl_args)
                pl.set_closed(self._is_yearmonth_old(current_yearmonth, created_yearmonth))
                songs_by_month[created_yearmonth] = pl
            songs_by_month[created_yearmonth].add_track(track.id)
        for m in sorted(songs_by_month.keys()):
            pl = songs_by_month[m]
            for p in pl.get_ingestable_playlists():
                new_playlists.append(p)
        return PlaylistGeneratorResults(delete_playlists, new_playlists)

    def _gen_most_played(self, config):
        if config.has_key('limit'):
            limit = min(config['limit'], Playlist.PLAYLIST_MAX)
        else:
            limit = Playlist.PLAYLIST_MAX
        include_playlists = False
        delete_playlists = self.library_db.get_generated_playlists("WHERE type='%s'" % (self.MOST_PLAYED))
        if config.has_key('include_playlists'):
            include_playlists = config['include_playlists']
        if include_playlists == True:
            self.logger.warn("Playlists not supported yet for most played")
        playlist = Playlist(self.full_playlist_name('Most played'), self.timestamp)
        playlist.set_type(self.MOST_PLAYED)
        for track in self.library_db.get_tracks("ORDER BY playCount DESC, recentTimestamp DESC LIMIT %d" % limit):
            playlist.add_track(track.id)
        return PlaylistGeneratorResults(delete_playlists, [playlist])
