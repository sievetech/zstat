# coding=utf-8

from zstat import modules

UNSUPPORTED = "ZBX_NOTSUPPORTED"


def find_metric_module(key):
    """
    Given a metric key, finds witch module knows how to process that metric key
    """

    function_name = key.replace(".", "_")
    module_name = key.split(".")[0]
    if hasattr(modules, module_name):
        _module = getattr(modules, module_name)
        return _module

    return None


def process_metric_key(key, *args):
    function_name = key.replace(".", "_")
    _module = find_metric_module(key)
    if not _module or not hasattr(_module, function_name):
        return UNSUPPORTED
    return getattr(_module, function_name)(*args)