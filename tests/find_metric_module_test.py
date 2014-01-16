# coding=utf-8

import unittest
from zstat import find_metric_module
from zstat.modules import mysql


class FindMetricModule(unittest.TestCase):

    def test_find_module_for_known_metric_key(self):
        self.assertEqual(mysql, find_metric_module("mysql.locks"))

    def test_return_none_for_unknown_metric_key(self):
        self.assertIsNone(find_metric_module("unknown.metric.key"))
