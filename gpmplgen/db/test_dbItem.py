from unittest import TestCase

from .dbitem import *

class TestDbItem(TestCase):
    def setUp(self):
        self.a = DbItem([
            DbColumn("a","b"),
            DbColumn("c","d")
        ])
        self.b = DbItem([
            DbColumn("c","d"),
            DbColumn("a","b")
        ])
        self.c = DbItem([
            DbColumn("c","d")
        ])

    def test_get_columns(self):
        self.assertEqual(self.a.get_columns(),"a,c")
        self.assertEqual(self.b.get_columns(),"c,a")
        self.assertEqual(self.c.get_columns(),"c")

    def test_get_schema(self):
        self.assertEqual(self.a.get_schema(),"(a B,c D)")
        self.assertEqual(self.b.get_schema(),"(c D,a B)")
        self.assertEqual(self.c.get_schema(),"(c D)")
