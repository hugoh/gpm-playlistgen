# -*- coding: utf-8 -*-

from unittest import TestCase
from .playlist_generator import PlaylistGenerator, PlaylistGeneratorError


class TestPlaylistGenerator(TestCase):
    def test_gen_full_name(self):
        plg = PlaylistGenerator(None, None, None)
        self.assertEqual(plg.full_playlist_name('foo'), 'foo')
        plg = PlaylistGenerator("", None, None)
        self.assertEqual(plg.full_playlist_name('foo'), 'foo')
        plg = PlaylistGenerator("bar", None, None)
        self.assertEqual(plg.full_playlist_name('foo'), 'bar foo')
        plg = PlaylistGenerator(u"…", None, None)
        self.assertEqual(plg.full_playlist_name('foo'), u"… foo")

    def test__gen_yearmonth(self):
        self.assertEqual(PlaylistGenerator._gen_yearmonth(1492295379), "2017-04")

    def test__is_yearmonth_old(self):
        self.assertTrue(PlaylistGenerator._is_yearmonth_old("2017-04", "2017-03"))
        self.assertTrue(PlaylistGenerator._is_yearmonth_old("2017-04", "2016-12"))
        self.assertFalse(PlaylistGenerator._is_yearmonth_old("2017-04", "2017-04"))
        self.assertFalse(PlaylistGenerator._is_yearmonth_old("2017-04", "2017-05"))

    def test_generate(self):
        plg = PlaylistGenerator(None, None, None)
        with self.assertRaises(PlaylistGeneratorError):
            plg.generate("non_existent", None)
        for supported_type in [ "monthly_added", "most_played" ]:
            try:
                plg.generate(supported_type, None)
            except TypeError:
                pass
            except AttributeError:
                pass
