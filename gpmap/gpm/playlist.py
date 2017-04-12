import itertools

class Playlist:
    PLAYLIST_MAX = 1000

    def __init__(self, name):
        self.name = name
        self.tracks = []

    def add_track(self, track):
        self.tracks.append(track)

    def get_ingestable_playlists(self):
        it = iter(self.tracks)
        item = list(itertools.islice(it, Playlist.PLAYLIST_MAX))
        total_count = 1 + len(self.tracks) / Playlist.PLAYLIST_MAX
        n = 1
        while item:
            name = self.name
            if total_count > 1:
                name += " (%d/%d)" % (n, total_count)
            pl = Playlist(name)
            pl.tracks = item
            yield pl
            item = list(itertools.islice(it, Playlist.PLAYLIST_MAX))
            n += 1