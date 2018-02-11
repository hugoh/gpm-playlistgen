from unittest import TestCase

from gpmplgen.db.dbitem import DbColumn

class TestDbColumn(TestCase):
    def setUp(self):
        self.c = DbColumn("a", "b")

    def test_get_name(self):
        self.assertEqual(self.c.get_name(), "a")

    def test_get_column_def(self):
        self.assertEqual(self.c.get_column_def(), "a B")
