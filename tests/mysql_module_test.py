# coding=utf-8
import unittest
import mock
from zstat.modules import mysql


class MysqlModuleTest(unittest.TestCase):

    def test_get_mysql_known_status(self):
        cursor_mock = mock.Mock()
        ctx = mock.MagicMock()
        ctx.__enter__.return_value = cursor_mock
        with mock.patch.object(mysql, "_get_cursor", return_value=ctx):
            cursor_mock.fetchall.return_value = [("Threads_connected", "1")]
            variable_value = mysql._get_mysql_status_value("Threads_connected")
            self.assertEqual([mock.call("SHOW STATUS WHERE `variable_name` = %s", ("Threads_connected",))], cursor_mock.execute.call_args_list)
            self.assertEqual("1", variable_value)

    def test_get_mysql_unknown_status(self):
        cursor_mock = mock.Mock()
        ctx = mock.MagicMock()
        ctx.__enter__.return_value = cursor_mock
        with mock.patch.object(mysql, "_get_cursor", return_value=ctx):
            cursor_mock.fetchall.return_value = []
            variable_value = mysql._get_mysql_status_value("UnKnown")
            self.assertEqual([mock.call("SHOW STATUS WHERE `variable_name` = %s", ("UnKnown",))], cursor_mock.execute.call_args_list)
            self.assertEqual("", variable_value)

    def test_get_mysql_generic_status(self):
        ctx = mock.MagicMock()
        with mock.patch.object(mysql, "_get_mysql_status_value", return_value=ctx):
            mysql.mysql_status("Innodb_buffer_pool_reads")
            self.assertEqual([mock.call("Innodb_buffer_pool_reads")], mysql._get_mysql_status_value.call_args_list)