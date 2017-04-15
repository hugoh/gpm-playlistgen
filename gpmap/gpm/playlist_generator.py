import datetime

from .playlist import Playlist

class PlaylistGenerator():
    def __init__(self, playlist_prefix, timestamp, library_db):
        self.playlist_prefix = playlist_prefix
        self.timestamp = timestamp
        self.library_db = library_db

    def gen_monthly_added(self, config):
        songsByMonth = {}
        for s in self.library_db.get_tracks("ORDER BY creationTimestamp, discNumber, trackNumber"):
            # Group by year & month
            created_time_ms = s.creation_timestamp
            created_time = created_time_ms / (10 ** 6)
            created_yearmonth = datetime.datetime.fromtimestamp(created_time).strftime('%Y-%m')
            if songsByMonth.has_key(created_yearmonth) == False:
                songsByMonth[created_yearmonth] = Playlist(self.playlist_prefix + ' Added in ' + created_yearmonth, self.timestamp)
            songsByMonth[created_yearmonth].add_track(s.id)
        ret = []
        for m in sorted(songsByMonth.keys()):
            pl = songsByMonth[m]
            for p in pl.get_ingestable_playlists():
                ret.append(pl)
        return ret
