from unittest import TestCase

from playlist import Playlist
import json


class TestPlaylist(TestCase):
    PREFIX = "[GPMAP]"
    NAME = "%s foo" % PREFIX
    GEN = 123456

    def setUp(self):
        self.sample_playlist = Playlist(self.NAME, self.GEN)

    def test_hasmax(self):
        self.assertTrue(Playlist.PLAYLIST_MAX > 0, "max set")

    def test_name(self):
        self.assertEqual(self.NAME, self.sample_playlist.get_name())

    def _test_playlist_value(self, playlist, version, generatedby, generated, playlist_type, args, closed):
        obj = json.loads(playlist.get_description())
        self.assertEqual(obj['version'], version)
        self.assertEqual(obj['generatedby'], generatedby)
        self.assertEqual(obj['generated'], generated)
        self.assertEqual(obj['type'], playlist_type)
        self.assertEqual(obj['args'], args)
        self.assertEqual(obj['closed'], closed)

    def test_description(self):
        pl = self.sample_playlist
        self._test_playlist_value(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, None, None, False)
        pl.set_type("foo")
        self._test_playlist_value(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, "foo", None, False)
        pl.set_args("bar")
        self._test_playlist_value(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, "foo", "bar", False)
        pl.set_closed()
        self._test_playlist_value(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, "foo", "bar", True)

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

    def test_generated_by_gpmap(self):
        self.assertTrue(Playlist.is_generated_by_gpmap({
            'name': self.sample_playlist.get_name(),
            'description': self.sample_playlist.get_description()
        }))

        desc = json.loads(self.sample_playlist.get_description())
        desc['version'] = 2
        self.assertFalse(Playlist.is_generated_by_gpmap({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        desc = json.loads(self.sample_playlist.get_description())
        del desc['version']
        self.assertFalse(Playlist.is_generated_by_gpmap({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        desc = json.loads(self.sample_playlist.get_description())
        del desc['generatedby']
        self.assertFalse(Playlist.is_generated_by_gpmap({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        self.assertFalse(Playlist.is_generated_by_gpmap({
            'name': self.sample_playlist.get_name(),
            'description': self.sample_playlist.get_description()[:-1]
        }))
