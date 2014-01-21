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


def rabbitmq_node_usedmempercent(*args):
    client = _get_client()
    node_info = client.http.do_call("nodes/{}".format(args[0]), "GET")
    return "{:2.2f}".format(float(node_info['mem_used']) / float(node_info['mem_limit']))


def rabbitmq_node_usedfdpercent(*args):
    client = _get_client()
    node_info = client.http.do_call("nodes/{}".format(args[0]), "GET")
    return "{:2.2f}".format(float(node_info['fd_used']) / float(node_info['fd_total']))


def rabbitmq_node_usedndpercent(*args):
    client = _get_client()
    node_info = client.http.do_call("nodes/{}".format(args[0]), "GET")
    return "{:2.2f}".format(float(node_info['sockets_used']) / float(node_info['sockets_total']))
