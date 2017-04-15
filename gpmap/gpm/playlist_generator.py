import datetime
import logging

from .playlist import Playlist

class PlaylistGenerator():
    MONTHLY_ADDED = 'monthly_added'
    MOST_PLAYED = 'most_played'

    def __init__(self, playlist_prefix, timestamp, library_db):
        self.logger = logging.getLogger(__name__)
        self.playlist_prefix = playlist_prefix
        self.timestamp = timestamp
        self.library_db = library_db

    def generate(self, type, config):
        gen_func = getattr(self, "_gen_" + type)
        return gen_func(self, config)

    def gen_full_name(self, name):
        if self.playlist_prefix != None and len(self.playlist_prefix) > 0:
            return self.playlist_prefix + ' ' + name
        else:
            return name

    def _gen_monthly_added(self, config):
        songsByMonth = {}
        for track in self.library_db.get_tracks("ORDER BY creationTimestamp, discNumber, trackNumber"):
            # Group by year & month
            created_time_ms = track.creationTimestamp
            created_time = created_time_ms / (10 ** 6)
            created_yearmonth = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m')
            if songsByMonth.has_key(created_yearmonth) == False:
                pl = Playlist(self.gen_full_name('Added in ' + created_yearmonth), self.timestamp)
                pl.set_type(self.MONTHLY_ADDED)
                pl.set_args(created_yearmonth)
                songsByMonth[created_yearmonth] = pl
            songsByMonth[created_yearmonth].add_track(track.id)
        ret = []
        for m in sorted(songsByMonth.keys()):
            pl = songsByMonth[m]
            for p in pl.get_ingestable_playlists():
                ret.append(p)
        return ret

    def _gen_most_played(self, config):
        if config.has_key('limit'):
            limit = min(config['limit'], Playlist.PLAYLIST_MAX)
        else:
            limit = Playlist.PLAYLIST_MAX
        include_playlists = False
        if config.has_key('include_playlists'):
            include_playlists = config['include_playlists']
        if include_playlists == True:
            self.logger.warn("Playlists not supported yet for most played")
        playlist = Playlist(self.gen_full_name('Most played'), self.timestamp)
        playlist.set_type(self.MOST_PLAYED)
        # FIXME: add recentTimestamp
        for track in self.library_db.get_tracks("ORDER BY playCount DESC LIMIT %d" % limit):
            playlist.add_track(track.id)
        return [playlist]
