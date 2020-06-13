#!/usr/bin/env python
# coding=utf-8
# author:

# %%
import math
import os
import sqlite3

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import settings
from lib.path import DATA_PATH

# %%
db_path = os.path.join(DATA_PATH, settings.DBNAME)
conn = sqlite3.connect(db_path)

plt.rcParams['figure.figsize'] = (18, 18)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号


def table_dataframe(table):
    return pd.read_sql_query(f"select * from {table};", conn)


def pie_range_count(data, label=None):
    """

    :param data:
    :param label:
    :return:
    """
    count = data.groupby(["range"])["houseID"].count().reset_index(name="count")
    plt.pie(count['count'].values, autopct='%.2f', label=label)


def plot_range_count(data, label=None):
    count = data.groupby(["range"])["houseID"].count().reset_index(name="count")
    plt.plot(count['range'], count['count'].values, label=label)


def price_yymm(data):
    data_group = data.groupby([data['dealdate'].map(lambda t: pd.datetime(t.year, t.month, 1))])
    data_group = data_group.agg({'totalPrice': np.sum, 'square': np.sum})
    data_group['price'] = data_group['totalPrice'] / data_group['square']
    data_group = data_group.reset_index()
    return data_group


def square_to_numeric(x):
    try:
        return float(x[:-2])
    except:
        return 0


# %% 在售房价
# df = table_dataframe('sellhouseinfo')
#
# df[['totalPrice', 'unitPrice']] = df[['totalPrice', 'unitPrice']].apply(pd.to_numeric)
# df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]
# df['range'] = df.totalPrice.map(lambda x: math.floor(float(x) / 10) / 10)
#
# plot_range_count(df)
# plt.title("在售总房价销量分布")
# plt.show()

# %% 已售
df = table_dataframe('soldhouseinfo')

# 总价、单价
df[['totalPrice', 'unitPrice', 'community']] = df[['totalPrice', 'unitPrice', 'community']].apply(pd.to_numeric)
df = df[(df.totalPrice > 0) & (df.totalPrice < 1000)]

df['dealdate'] = df['dealdate'].apply(pd.to_datetime)
df = df[df.dealdate > pd.datetime(2015, 1, 1)]

# 面积
df['square'] = df.square.map(lambda x: square_to_numeric(x))
df = df[(df.square != 0)]

# 交易总价分片
df['range'] = df.totalPrice.map(lambda x: math.floor(float(x) / 10) / 10)

# 区县数据
community_df = table_dataframe('community')
df = pd.merge(df, community_df, left_on='community', right_on="id")

# 年度
years = sorted(set(df['dealdate'].dt.year))

# 区县
districts = set(community_df['district'])

# %% 已售总房价销量分布

plt.figure(1)
plt.title("已售总房价销量分布")
plot_range_count(df)
# plt.show()

# %%

plt.figure(2)
plt.title(f"已售总房价销量分布(2016-2019)")
for year in years:
    plot_range_count(df[df['dealdate'].dt.year == year], label=year)
plt.legend(loc=0)

# plt.show()

# %% 已售均价

price = price_yymm(df)

# for year in years:
#     data_y = price[price['dealdate'].dt.year == year]
#     plt.plot(data_y['dealdate'], data_y['price'], label=year)
# plt.title(f"已售均价(2016-2019)")
# plt.legend(loc=0)
# plt.show()

plt.figure(3)
plt.title(f"已售均价")
plt.plot(price['dealdate'], price['price'])


# plt.show()


# %% 房屋销售量

def count_yymm(data):
    # data_group = data.groupby([data['dealdate'].map(lambda t: pd.datetime(t.year, t.month, 1))])
    data_group = data.groupby([data.dealdate.dt.year, data.dealdate.dt.month])
    data_group = data_group["houseID"].count().reset_index(name="count")
    return data_group


count_yymm1 = count_yymm(df)
for year in years:
    line = count_yymm1[count_yymm1['dealdate'].dt.year == year]
    plt.plot(line['dealdate'], line['count'].values, label=year)
plt.legend(loc=0)
plt.title(f"房屋销售量分布(2016-2019)")
plt.show()

# count_yymm1 = count_yymm(df)
# plt.figure(4)
# plt.title(f"房屋销售量分布")
# plt.plot(count_yymm1['dealdate'], count_yymm1['count'].values)
# plt.show()

# %% 区县

# 区县总价
plt.figure(5)
plt.title("区县已售总房价销量分布")

for district in districts:
    df_d = df[df.district == district]
    plot_range_count(df_d, label=district)

plt.legend(loc=0)

# plt.show()

# 区县已售均价
plt.figure(6)
plt.title(f"区县已售均价(2016-2019)")

for district in districts:
    df_d = df[df.district == district]
    price = price_yymm(df_d)
    plt.plot(price['dealdate'], price['price'], label=district)

plt.legend(loc=0)

# plt.show()

plt.figure(7)
plt.title(f"区县房屋销售量分布")

for district in districts:
    df_d = df[df.district == district]
    line = count_yymm(df_d)
    plt.bar(line['dealdate'], line['count'].values, label=district)
    # df.groupby([df_d.dealdate.dt.year, df_d.dealdate.dt.month]).houseID.value_counts().unstack(0)
    # tmp = df_d['dealdate'].groupby([df_d.dealdate.dt.year, df_d.dealdate.dt.month]).agg('count')
    # tmp2 = [f'{x}-{y}' for x, y in tmp.index]
    # plt.bar(tmp2, tmp.values, label=district)
    # plt.xticks(rotation=60)

# df.groupby([df_d.dealdate.dt.year, df_d.dealdate.dt.month]).houseID.value_counts().unstack(0).plot.bar()

plt.legend(loc=0)

plt.show()

# %% 小区销量

tmp = df[(df.district == '松江') & (df.dealdate > '2019-8-1')]

tmp.groupby('community').size().reset_index(name='size').sort_values('size')
