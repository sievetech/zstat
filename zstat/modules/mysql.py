# coding=utf-8
import sys
import MySQLdb
from zstat.settings import config


mysql_config_opts = config.get("mysql", {})
USER = mysql_config_opts.get("user", "root")
PWD = mysql_config_opts.get("pwd", "")
HOST = mysql_config_opts.get("host", "127.0.0.1")


def _get_cursor():
    connect = MySQLdb.connect(host=HOST, port=3306, user=USER, passwd=PWD)
    cursor = connect.cursor()
    return cursor


def _get_mysql_variable(variable_name):
    c = _get_cursor()
    c.execute("SHOW STATUS WHERE `variable_name` = '{}'".format(variable_name))
    data = c.fetchall()
    if data:
        return data[0][1]
    return ""


def process(key, *args):
    function_name = key.replace(".", "_")
    available_functioons = sys.modules[__name__].__dict__
    if function_name not in available_functioons:
        return None
    return available_functioons[function_name](*args)


def mysql_connections(*args):
    return _get_mysql_variable("Threads_connected")
