# coding=utf-8
from pyrabbit.api import Client
from zstat.settings import config

rabbit_options = config.get("rabbitmq", {})

host = rabbit_options.get("host", "localhost")
port = rabbit_options.get("port", "55672")
user = rabbit_options.get("user", "guest")
passwd = rabbit_options.get("pwd", "guest")


def _get_client():
    return Client("{}:{}".format(host, port), user, passwd)


def rabbitmq_totalmsg(*args):
    client = _get_client()
    if args and len(args) == 2:  # Host and queue-name
        return client.get_queue(args[0], args[1])['messages']
    return client.get_overview()['queue_totals']['messages']


def rabbitmq_redelivery(*args):
    client = _get_client()
    return client.get_overview()['message_stats']['redeliver_details']['rate']


def _get_node_info(node_name):
    client = _get_client()
    node_info = client.http.do_call("nodes/{}".format(node_name or ""), "GET")
    return node_info if node_name else node_info[0]


def rabbitmq_node_usedmempercent(*args):
    node_name = args[0] if args else None
    node_info = _get_node_info(node_name)
    return "{:2.2f}".format(float(node_info['mem_used']) / float(node_info['mem_limit']))


def rabbitmq_node_usedfdpercent(*args):
    """
    Usage of file descritpors (%)
    """
    node_name = args[0] if args else None
    node_info = _get_node_info(node_name)
    return "{:2.2f}".format(float(node_info['fd_used']) / float(node_info['fd_total']))


def rabbitmq_node_usedndpercent(*args):
    """
    Usage of network descritpors (%)
    """
    node_name = args[0] if args else None
    node_info = _get_node_info(node_name)
    return "{:2.2f}".format(float(node_info['sockets_used']) / float(node_info['sockets_total']))
