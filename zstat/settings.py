# coding=utf-8

from ConfigParser import SafeConfigParser
import os

CONFIG_PATH = os.path.expanduser("~/.zstat.cfg")


def read_config_file(config_file=CONFIG_PATH):
    values_dict = {}
    cfg = SafeConfigParser()
    cfg.read(config_file)
    for section in cfg.sections():
        values_dict[section] = {k: v for (k, v) in cfg.items(section)}
    return values_dict


config = read_config_file(CONFIG_PATH)






