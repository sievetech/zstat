# coding=utf-8
import os
import unittest
from zstat.settings import read_config_file

HERE = os.path.abspath(os.path.dirname(__file__))


class SettingsTest(unittest.TestCase):

    def test_empty_config(self):
        self.assertEqual({}, read_config_file(os.path.join(HERE, "empty.cfg")))

    def test_ransform_to_dicts(self):
        cfg_values = read_config_file(os.path.join(HERE, "data/config.cfg"))
        mysql_options = {"user": "root",
                         "pwd": "",
                         "host": "127.0.0.1"}
        self.assertEqual(mysql_options, cfg_values['mysql'])
