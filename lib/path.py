#!/usr/bin/env python
# coding=utf-8

import inspect
import os
import sys


def get_root_path():
    file_path = os.path.abspath(inspect.getfile(sys.modules[__name__]))
    lib_path = os.path.dirname(file_path)
    root_path = os.path.dirname(lib_path)
    return root_path


def create_date_path(site, city, date):
    root_path = get_root_path()
    date_path = "{}/data/{}.{}/{}".format(root_path, city, site, date)
    if not os.path.exists(date_path):
        os.makedirs(date_path)
    print(date_path)
    return date_path


# const for path
ROOT_PATH = get_root_path()
DATA_PATH = ROOT_PATH + "/data"

if __name__ == "__main__":
    create_date_path("lianjia", "sh", "20160912")
    create_date_path("anjuke", "bj", "20160912")
