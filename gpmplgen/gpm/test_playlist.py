from unittest import TestCase

from playlist import Playlist
import json


class TestPlaylist(TestCase):
    PREFIX = "FOO"
    NAME = "%s foo" % PREFIX
    GEN = 123456
    TYPE = 'foo'
    ARGS = 'bar'

    def setUp(self):
        self.sample_playlist = Playlist(self.NAME, self.GEN)

    def test_hasmax(self):
        self.assertTrue(Playlist.PLAYLIST_MAX > 0, "max set")

    def test_name(self):
        self.assertEqual(self.NAME, self.sample_playlist.get_name())

    def _test_playlist_description(self, playlist, version, generatedby, generated, playlist_type, args, final):
        obj = json.loads(playlist.get_description())
        self.assertEqual(obj['version'], version)
        self.assertEqual(obj['generatedby'], generatedby)
        self.assertEqual(obj['generated'], generated)
        self.assertEqual(obj['type'], playlist_type)
        self.assertEqual(obj['args'], args)
        self.assertEqual(obj['final'], final)

    def test_description(self):
        pl = self.sample_playlist
        self._test_playlist_description(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, None, None, False)
        pl.set_type(self.TYPE)
        self._test_playlist_description(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, self.TYPE, None, False)
        pl.set_args(self.ARGS)
        self._test_playlist_description(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, self.TYPE, self.ARGS, False)
        pl.set_final()
        self._test_playlist_description(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, self.TYPE, self.ARGS, True)

    def test_get_ingestable_playlist(self):
        list_count = 3
        extra_count = 5
        total_count = Playlist.PLAYLIST_MAX * (list_count - 1) + extra_count
        for i in xrange(total_count):
            self.sample_playlist.add_track(i)
        i = 0
        self.sample_playlist.set_type(self.TYPE)
        self.sample_playlist.set_args(self.ARGS)
        self.sample_playlist.set_final()
        for pl in self.sample_playlist.get_ingestable_playlists():
            i += 1
            expected_name = "%s (%d/%d)" % (self.NAME, i, list_count)
            self.assertEqual(expected_name, pl.get_name(), msg='{0} != {1}'.format(expected_name, pl.get_name()))
            self._test_playlist_description(pl, Playlist.VERSION, Playlist.GENERATEDBY, self.GEN, self.TYPE, self.ARGS, True)
            if (i != list_count):
                l = Playlist.PLAYLIST_MAX
            else:
                l = extra_count
            self.assertEqual(len(pl.tracks), l, "correct length")
        self.assertEqual(list_count, i, "correct number of playlists")

    def test_generated_by_gpmplgen(self):
        self.assertTrue(Playlist.is_generated_by_gpmplgen({
            'name': self.sample_playlist.get_name(),
            'description': self.sample_playlist.get_description()
        }))

        desc = json.loads(self.sample_playlist.get_description())
        desc['version'] = 2
        self.assertFalse(Playlist.is_generated_by_gpmplgen({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        desc = json.loads(self.sample_playlist.get_description())
        del desc['version']
        self.assertFalse(Playlist.is_generated_by_gpmplgen({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        desc = json.loads(self.sample_playlist.get_description())
        del desc['generatedby']
        self.assertFalse(Playlist.is_generated_by_gpmplgen({
            'name': self.sample_playlist.get_name(),
            'description': json.dumps(desc)
        }))

        self.assertFalse(Playlist.is_generated_by_gpmplgen({
            'name': self.sample_playlist.get_name(),
            'description': self.sample_playlist.get_description()[:-1]
        }))
