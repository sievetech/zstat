# coding=utf-8

import sys
from zstat import process_metric_key, UNSUPPORTED


def main():
    print str(process_metric_key(*sys.argv[1:])) or UNSUPPORTED


if __name__ == "__main__":
    main()