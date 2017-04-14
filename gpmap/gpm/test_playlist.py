import unittest
from playlist import Playlist
import json

class TestPlaylist(unittest.TestCase):

    NAME = "foo"
    GEN = 123456

    def setUp(self):
        self.sample_playlist = Playlist(self.NAME, self.GEN)

    def test_hasmax(self):
        self.assertTrue(Playlist.PLAYLIST_MAX > 0, "max set")

    def test_name(self):
        self.assertEqual(self.NAME, self.sample_playlist.get_name())

    def test_description(self):
        description = self.sample_playlist.get_description()
        obj = json.loads(description)
        self.assertEqual(obj['version'], Playlist.VERSION)
        self.assertEqual(obj['generatedby'], Playlist.GENERATEDBY)
        self.assertEqual(obj['generated'], self.GEN)

    def test_get_ingestable_playlist(self):
        list_count = 3
        extra_count = 5
        total_count = Playlist.PLAYLIST_MAX * (list_count - 1) + extra_count
        for i in xrange(total_count):
            self.sample_playlist.add_track(i)
        i = 0
        for pl in self.sample_playlist.get_ingestable_playlists():
            i += 1
            self.assertEqual("%s (%d/%d)" % (self.NAME, i, list_count), pl.get_name(), "correct name")
            if (i != list_count):
                l = Playlist.PLAYLIST_MAX
            else:
                l = extra_count
            self.assertEqual(len(pl.tracks), l, "correct length")
        self.assertEqual(list_count, i, "correct number of playlists")