from unittest import TestCase

from gpmplgen.config import *

class TestConfig(TestCase):
    def setUp(self):
        self.config_utf8 = Config()
        test_utf8_config = "tests/test-config-utf8.yaml"
        with open(test_utf8_config, encoding='utf-8') as fd:
            self.config_utf8.fromYaml(fd)
            fd.close()

    def test_get_columns(self):
        self.assertEquals(self.config_utf8.playlist_prefix, "♽")
