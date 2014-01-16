# coding=utf-8
import unittest
import mock
from zstat.modules import mysql


class MysqlModuleTest(unittest.TestCase):

    def test_mysql_connections(self):
        #mysql.process("mysql.connections")
        self.fail()

    def test_get_mysql_known_variable(self):
        cursor_mock = mock.Mock()
        with mock.patch.object(mysql, "_get_cursor", return_value=cursor_mock):
            cursor_mock.fetchall.return_value = [("Threads_connected", "1")]
            variable_value = mysql._get_mysql_variable("Threads_connected")
            self.assertEqual([mock.call("SHOW STATUS WHERE `variable_name` = 'Threads_connected'")], cursor_mock.execute.call_args_list)
            self.assertEqual("1", variable_value)

    def test_get_mysql_unknown_variable(self):
        cursor_mock = mock.Mock()
        with mock.patch.object(mysql, "_get_cursor", return_value=cursor_mock):
            cursor_mock.fetchall.return_value = []
            variable_value = mysql._get_mysql_variable("UnKnown")
            self.assertEqual([mock.call("SHOW STATUS WHERE `variable_name` = 'UnKnown'")], cursor_mock.execute.call_args_list)
            self.assertEqual("", variable_value)