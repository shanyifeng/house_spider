#!/usr/bin/env python
# coding=utf-8
# author: 

import math
import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd

import settings
from lib.path import DATA_PATH

# %%
db_path = os.path.join(DATA_PATH, settings.DBNAME)
conn = sqlite3.connect(db_path)

plt.figure(figsize=(18, 18))
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def table_dataframe(table):
    return pd.read_sql_query(f"select * from {table};", conn)


# %%
df = table_dataframe('sellhouseinfo')
df[['totalPrice', 'unitPrice']] = df[['totalPrice', 'unitPrice']].apply(pd.to_numeric)

df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]
df['range'] = df.totalPrice.map(lambda x: math.floor(float(x) / 10) / 10)

count = df.groupby(["range"])["houseID"].count().reset_index(name="count")
plt.pie(count['count'], labels=count['range'], autopct='%.2f')
plt.show()
plt.plot(count['range'], count['count'])
plt.show()

# %%
df = table_dataframe('soldhouseinfo')
df[['totalPrice', 'unitPrice']] = df[['totalPrice', 'unitPrice']].apply(pd.to_numeric)

df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]
df['range'] = df.totalPrice.map(lambda x: math.floor(float(x) / 10) / 10)
df['dealyear'] = df.dealdate.str[:4]
df['dealmonth'] = df.dealdate.str[5:7]

# %%
tmp = df[df.dealyear > '2015']
df1 = tmp.groupby(['dealyear', 'range'])["houseID"].count().reset_index(name="count")
for year in ['2016', '2017', '2018', '2019']:
    line = df1[df1.dealyear == year]
    idx = [i for i in range(len(line['range']))]
    plt.plot(idx, line['count'].values, label=year)
    # plt.suptitle(year)
plt.legend(loc=0)
plt.show()


# %%
def plot_range(df):
    tmp = df.groupby(["range"])["houseID"].count().reset_index(name="count")
    tmp.index = count['range']
    tmp.plot.pie(y='count', figsize=(6, 6), autopct='%.2f')


def plot_price(df, label=None):
    dfg = df.groupby(['dealyear', 'dealmonth'])
    totalPrice = dfg["totalPrice"].sum().reset_index(name="totalPrice")
    squaref = dfg["squaref"].sum().reset_index(name="squaref")
    price = totalPrice.totalPrice / squaref.squaref
    plt.plot(price, label=label)


def plot_range_count(df, label=None):
    count = df.groupby(["range"])["houseID"].count().reset_index(name="count")
    plt.plot.pie(count['range'], count['count'].values, label=label)


def plot_range_pie(df):
    count = df.groupby(["range"])["houseID"].count().reset_index(name="count")
    plt.pie(count['count'].values, autopct='%.2f')


# year = '2019'
# plot_range(df[df.dealdate.str.startswith(year)])
# plt.suptitle(year)
# plt.show()

# %%

tmp = df[df.dealyear > '2015']
df1 = tmp.groupby(['dealyear', 'dealmonth'])["houseID"].count().reset_index(name="count")

for year in set(tmp.dealyear):
    line = df1[df1.dealyear == year]
    plt.plot(line['dealmonth'], line['count'].values, label=year)
plt.legend(loc=0)
plt.show()


# %%
def f_value(x):
    try:
        return float(x[:-2])
    except:
        return 0


df['squaref'] = df.square.map(lambda x: f_value(x))
df = df[(df.squaref != 0)]

tmp = df[df.dealyear > '2015']
plot_price(tmp)
plt.show()

communitydf = table_dataframe('community')
for community in set(communitydf['district']):
    communityid = set(communitydf[communitydf.district == community]['id'])
    communityid = [str(id) for id in communityid]
    df1 = tmp[tmp['community'].isin(communityid)]
    plot_price(df1, label=community)
plt.legend(loc=0)
plt.show()

for community in set(communitydf['district']):
    communityid = set(communitydf[communitydf.district == community]['id'])
    communityid = [str(id) for id in communityid]
    df1 = tmp[tmp['community'].isin(communityid)]
    plot_range_count(df1, label=community)
plt.legend(loc=0)
plt.show()

for community in set(communitydf['district']):
    communityid = set(communitydf[communitydf.district == community]['id'])
    communityid = [str(id) for id in communityid]
    df1 = tmp[tmp['community'].isin(communityid)]
    plot_range_pie(df1, label=community)
plt.legend(loc=0)
plt.show()

for year in set(tmp.dealyear):
    df1 = tmp[tmp.dealyear == year]
    plot_price(df1, label=year)
plt.legend(loc=0)
plt.show()
