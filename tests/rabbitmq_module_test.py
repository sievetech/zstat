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