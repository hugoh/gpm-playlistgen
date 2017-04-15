import itertools
import json
import logging

class Playlist:
    VERSION = 1
    GENERATEDBY = 'GPMAP'
    PLAYLIST_MAX = 1000

    def __init__(self, name, generated):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.generated = generated
        self.tracks = []

    def get_name(self):
        return self.name

    def get_description(self):
        description = {
            'version': Playlist.VERSION,
            'generatedby': Playlist.GENERATEDBY,
            'generated': self.generated
        }
        return json.dumps(description)

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
            pl = Playlist(name, self.generated)
            pl.tracks = item
            yield pl
            item = list(itertools.islice(it, Playlist.PLAYLIST_MAX))
            n += 1

    @staticmethod
    def is_generated_by_gpmap(playlist_dict, prefix):
        if len(prefix) == 0:
            raise Exception('invalid prefix')
        if not playlist_dict['name'].startswith(prefix):
            return False
        try:
            desc = json.loads(playlist_dict['description'])
            if desc['version'] == Playlist.VERSION and desc['generatedby'] == Playlist.GENERATEDBY:
                return True
        except:
            return False
        return False

    def create_in_gpm(self, client):
        self.logger.info("Creating playlist " + self.get_name())
        playlist_id = client.create_playlist(self.get_name(), description=self.get_description())
        client.add_songs_to_playlist(playlist_id, self.tracks)