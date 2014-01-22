# coding=utf-8
import unittest
import mock

from zstat.modules import rabbitmq


class MysqlModuleTest(unittest.TestCase):

    def setUp(self):
        self._get_client_patch = mock.patch.object(rabbitmq, '_get_client')
        self._get_client_patch.start()
        self.client_mock = mock.MagicMock()
        rabbitmq._get_client.return_value = self.client_mock

    def tearDown(self):
        self._get_client_patch.stop()

    def test_get_rabbitmq_total_msg_without_vhost(self):
        self.client_mock.get_overview.return_value = {u'queue_totals': {u'messages': 21294,
                                                                        u'messages_ready': 20436,
                                                                        u'messages_unacknowledged': 858
                                                                        }
                                                      }
        value = rabbitmq.rabbitmq_totalmsg()
        self.assertEqual(21294, value)


    def test_get_rabbitmq_total_msg_one_queue(self):
        self.client_mock.get_overview.return_value = {u'queue_totals': {u'messages': 21294,
                                                                        u'messages_ready': 20436,
                                                                        u'messages_unacknowledged': 858
                                                                        }
                                                      }
        self.client_mock.get_queue.return_value = {"messages": 42}
        value = rabbitmq.rabbitmq_totalmsg("/", "extractor")
        self.assertEqual(42, value)

    def test_rabbitmq_redelivery_rate(self):
        self.client_mock.get_overview.return_value = {u'queue_totals': {u'messages': 21294,
                                                                        u'messages_ready': 20436,
                                                                        u'messages_unacknowledged': 858
                                                                        },
                                                      u'message_stats': {
                                                          u'redeliver_details': {
                                                              u'rate': 0.34
                                                          }
                                                      }
                                                      }
        value = rabbitmq.rabbitmq_redelivery()
        self.assertEqual(0.34, value)

    def test_rabbitmq_usedmempercent_with_node_name(self):
        self.client_mock.http.do_call.return_value = {"mem_used": 3, "mem_limit": 10}
        value = rabbitmq.rabbitmq_node_usedmempercent("rabbitmq@my-node")
        self.assertEqual([mock.call("nodes/rabbitmq@my-node", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.30", value)

    def test_rabbitmq_usedmempercent_without_node_name(self):
        self.client_mock.http.do_call.return_value = [{"mem_used": 4, "mem_limit": 10}]
        value = rabbitmq.rabbitmq_node_usedmempercent()
        self.assertEqual([mock.call("nodes/", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.40", value)

    def test_rabbitmq_usedfdpercent_with_node_name(self):
        """
        Used file descriptors
        """
        self.client_mock.http.do_call.return_value = {"fd_used": 5, "fd_total": 10}
        value = rabbitmq.rabbitmq_node_usedfdpercent("rabbitmq@my-node")
        self.assertEqual([mock.call("nodes/rabbitmq@my-node", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.50", value)

    def test_rabbitmq_usedfdpercent_without_node_name(self):
        """
        Used file descriptors
        """
        self.client_mock.http.do_call.return_value = [{"fd_used": 6, "fd_total": 10}]
        value = rabbitmq.rabbitmq_node_usedfdpercent()
        self.assertEqual([mock.call("nodes/", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.60", value)

    def test_rabbitmq_usedndpercent_with_node_name(self):
        """
        Used network descriptors
        """
        self.client_mock.http.do_call.return_value = {"sockets_used": 8, "sockets_total": 10}
        value = rabbitmq.rabbitmq_node_usedndpercent("rabbitmq@my-node")
        self.assertEqual([mock.call("nodes/rabbitmq@my-node", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.80", value)

    def test_rabbitmq_usedndpercent_without_node_name(self):
        """
        Used network descriptors
        """
        self.client_mock.http.do_call.return_value = [{"sockets_used": 9, "sockets_total": 10}]
        value = rabbitmq.rabbitmq_node_usedndpercent()
        self.assertEqual([mock.call("nodes/", "GET")], self.client_mock.http.do_call.call_args_list)
        self.assertEqual("0.90", value)

