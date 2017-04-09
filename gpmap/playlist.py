class Playlist:
    def __init__(self, name):
        self.name = name
        self.tracks = []

    def add_track(self, db_track):
        self.tracks.append(db_track)

    