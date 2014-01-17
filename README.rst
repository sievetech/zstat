zstat
=====

Set of metric collectors to be sent to the Zabbix_ monitoring system

.. _Zabbix: http://www.zabbix.com/download.php


How to Use
==========

Just call zsat with the metric name as the first argument

    $ zstat mysql.connections


Implemented modules
===================

mysql
*****

  * mysql.connections
  * mysql.locks

