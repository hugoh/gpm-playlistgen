import unittest
from playlist import Playlist
import json

class TestPlaylist(unittest.TestCase):

    NAME = "foo"
    GEN = 123456

    def setUp(self):
        self.samplePlaylist = Playlist(self.NAME, self.GEN)

    def test_hasmax(self):
        self.assertTrue(Playlist.PLAYLIST_MAX > 0, "max set")

    def test_name(self):
        self.assertEqual(self.NAME, self.samplePlaylist.get_name())

    def test_description(self):
        description = self.samplePlaylist.get_description()
        obj = json.loads(description)
        self.assertEqual(obj['version'], Playlist.VERSION)
        self.assertEqual(obj['generatedby'], Playlist.GENERATEDBY)
        self.assertEqual(obj['generated'], self.GEN)