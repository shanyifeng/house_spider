#!/usr/bin/env python
# coding=utf-8
# author: 

import os
import sqlite3
import settings
# import seaborn as sns
import pandas as pd
import numpy as np
from numpy.random import randn
import matplotlib as mpl
import matplotlib.pyplot as plt
# from scipy import stats
from lib.path import DATA_PATH

# %%
db_path = os.path.join(DATA_PATH, settings.DBNAME)
conn = sqlite3.connect(db_path)


def table_dataframe(table):
    return pd.read_sql_query(f"select * from {table};", conn)


# %%
df = table_dataframe('sellhouseinfo')
df[['totalPrice', 'unitPrice']] = df[['totalPrice', 'unitPrice']].apply(pd.to_numeric)


# %%
df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]
df['range'] = pd.cut(df['totalPrice'], 10)
count = df.groupby(["range"])["houseID"].count().reset_index(name="count")

# %%
# plt.kdeplot(count)
count.plot()
# plt.plot(data=count)
plt.show()


# %%
df = table_dataframe('soldhouseinfo')
df[['totalPrice', 'unitPrice']] = df[['totalPrice', 'unitPrice']].apply(pd.to_numeric)


# %%
df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]
df['range'] = pd.cut(df['totalPrice'], 10)

# %%
# plt.kdeplot(count)
year = '2019'
tmp = df[df.dealdate.str.startswith(year)]
count = tmp.groupby(["range"])["houseID"].count().reset_index(name="count")
count.index=count['range']
count.plot.pie(y='count',figsize=(6, 6), autopct='%.2f')
# plt.plot(data=count)
plt.suptitle(year)
plt.show()


#%%
df['dealyear'] = df.dealdate.str[:4]
year = df.groupby(["dealyear"])["houseID"].count().reset_index(name="count")
year.index = year['dealyear']
year.plot.pie(y='count',figsize=(6, 6), autopct='%.2f')
plt.suptitle("year")
plt.show()