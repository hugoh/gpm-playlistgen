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
        self.type = None
        self.args = None
        self.closed = False

    def get_name(self):
        return self.name

    def set_type(self, type):
        self.type = type

    def set_args(self, args):
        self.args = args

    def get_description(self):
        description = {
            'version': Playlist.VERSION,
            'generatedby': Playlist.GENERATEDBY,
            'generated': self.generated,
            'type': self.type,
            'args': self.args,
            'closed': self.closed
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
    def is_generated_by_gpmap(playlist_dict):
        try:
            desc = json.loads(playlist_dict['description'])
            if desc['generatedby'] == Playlist.GENERATEDBY:
                if desc['version'] == Playlist.VERSION:
                   return True
                else:
                    logging.warn("Unsupported version")
        except:
            return False
        return False

    def create_in_gpm(self, client):
        self.logger.info("Creating playlist " + self.get_name())
        playlist_id = client.create_playlist(self.get_name(), description=self.get_description())
        client.add_songs_to_playlist(playlist_id, self.tracks)