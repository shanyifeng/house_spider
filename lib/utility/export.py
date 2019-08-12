#!/usr/bin/env python
# coding=utf-8
# author: 

import os
from playhouse.dataset import DataSet

import settings
from lib.path import DATA_PATH

db_path = os.path.join(DATA_PATH, settings.DBNAME)
db = DataSet(f'sqlite:///{db_path}')


def export_table(name):
    table = db[name]
    csv_path = os.path.join(DATA_PATH, f'{name}.csv')
    db.freeze(table.all(), format='csv', filename=csv_path)
