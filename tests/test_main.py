# coding=utf-8
import unittest
import mock
from zstat import main


class MainTest(unittest.TestCase):

    def test_return_zero_metric(self):
        with mock.patch.object(main, "process_metric_key", return_value=0), \
             mock.patch("sys.stdout") as stdout_mock:
            main.main()
            self.assertEqual([mock.call("0"), mock.call("\n")], stdout_mock.write.call_args_list)
