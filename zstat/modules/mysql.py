# coding=utf-8
from contextlib import contextmanager
import MySQLdb
from zstat.settings import config


mysql_config_opts = config.get("mysql", {})
USER = mysql_config_opts.get("user", "root")
PWD = mysql_config_opts.get("pwd", "")
HOST = mysql_config_opts.get("host", "localhost")

@contextmanager
def _get_cursor():
    with MySQLdb.connect(host=HOST, port=3306, user=USER, passwd=PWD) as cursor:
        yield cursor


def _get_mysql_status_value(variable_name):
    with _get_cursor() as c:
        c.execute("SHOW STATUS WHERE `variable_name` = %s", (variable_name,))
        data = c.fetchall()
        if data:
            return data[0][1]
        return ""


def _get_mysql_slave_status_value(variable_name):
    with _get_cursor() as c:
        c.execute("SHOW SLAVE STATUS")
        column_names = [column[0].lower() for column in c.description]
        data = c.fetchall()
        if data and variable_name.lower() in column_names:
            return data[0][column_names.index(variable_name.lower())]
        return ""


def _query_result(query, *args):
    with _get_cursor() as c:
        c.execute(query, args)
        data = c.fetchall()
        if data:
            return data[0][0]
        return ""


def mysql_connections(*args):
    if args:
        place_holders = ",".join((" %s" * len(args)).split())
        query = "select count(1) from information_schema.processlist where user in ({})".format(place_holders)
        return _query_result(query, *args)
    return _get_mysql_status_value("Threads_connected")


def mysql_locks(*args):
    return _get_mysql_status_value("Innodb_row_lock_current_waits")


def mysql_rowsupdated(*args):
    return _get_mysql_status_value("Innodb_rows_updated")


def mysql_slowqueries(*args):
    return _get_mysql_status_value("Slow_queries")


def mysql_freemem(*args):
    return int(_get_mysql_status_value("Innodb_page_size")) * int(_get_mysql_status_value("Innodb_buffer_pool_pages_free"))


def mysql_updatepersecond(*args):
    return int(_get_mysql_status_value("Innodb_rows_updated")) / int(_get_mysql_status_value("Uptime"))


def mysql_insertpersecond(*args):
    return int(_get_mysql_status_value("Innodb_rows_inserted")) / int(_get_mysql_status_value("Uptime"))


def mysql_deletepersecond(*args):
    return int(_get_mysql_status_value("Innodb_rows_deleted")) / int(_get_mysql_status_value("Uptime"))


def mysql_slavestatus(column_name):
    return _get_mysql_slave_status_value(column_name)


def mysql_status(*args):
    if args:
        return _get_mysql_status_value(args[0])
    return ""