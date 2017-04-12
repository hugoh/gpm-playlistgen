import unittest
from playlist import Playlist

class TestPlaylist(unittest.TestCase):
    def test_hasmax(self):
        self.assertTrue(Playlist.PLAYLIST_MAX > 0, "max set")