# coding=utf-8

from ConfigParser import SafeConfigParser
import os

CONFIG_PATH = os.path.expanduser("~/.zstat.cfg")

config = SafeConfigParser()
config.read(CONFIG_PATH)






