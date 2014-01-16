# coding=utf-8

from zstat import modules

UNSUPPORTED = "ZBX_NOTSUPPORTED"


def find_metric_module(key):
    """
    Given a metric key, finds witch module knows how to process that metric key
    """

    module_name = key.split(".")[0]
    if hasattr(modules, module_name):
        _module = getattr(modules, module_name)
        if hasattr(_module, "process"):
            return _module

    return None


def process_metric_key(key, *args):
    _module = find_metric_module(key)
    if not _module:
        return UNSUPPORTED
    return _module.process(key, *args)