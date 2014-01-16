# coding=utf-8

import unittest
import mock
from zstat import process_metric_key, UNSUPPORTED


class ProcessMetricKeyTest(unittest.TestCase):

    def test_return_unsopprted_unknwon_metric_key(self):
        self.assertEqual(UNSUPPORTED, process_metric_key("unknown.metric.key"))

    def test_process_known_metric_key(self):
        with mock.patch("zstat.modules.mysql.process", return_value="42"):
            self.assertEqual("42", process_metric_key("mysql.connections"))
