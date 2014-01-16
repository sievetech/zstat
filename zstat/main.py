# coding=utf-8

import sys
from zstat import process_metric_key


def main():
    print process_metric_key(sys.argv[1:])