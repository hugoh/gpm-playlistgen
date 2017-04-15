# -*- coding: utf-8 -*-

from unittest import TestCase
from .playlist_generator import PlaylistGenerator


class TestPlaylistGenerator(TestCase):
    def test_gen_full_name(self):
        plg = PlaylistGenerator(None, None, None)
        self.assertEqual(plg.gen_full_name('foo'), 'foo')
        plg = PlaylistGenerator("", None, None)
        self.assertEqual(plg.gen_full_name('foo'), 'foo')
        plg = PlaylistGenerator("bar", None, None)
        self.assertEqual(plg.gen_full_name('foo'), 'bar foo')
        plg = PlaylistGenerator(u"…", None, None)
        self.assertEqual(plg.gen_full_name('foo'),  u"… foo")