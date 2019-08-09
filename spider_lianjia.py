#!/usr/bin/env python
# coding=utf-8
# author:
from gevent import monkey;
monkey.patch_all()

import logging
from lib import models, path

from lib.spider.lianjia.crawl_area import get_areas
from lib.spider.lianjia.crawl_tools import get_chengjiao_by_community, get_ershoufang_by_community, \
    get_community_list, get_community_info, get_chengjiao_house_info, get_ershou_house_info

log_format = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
logging.basicConfig(format=log_format, level=logging.INFO)

print(path.ROOT_PATH)

city = 'sh'
# districts = get_district_from_city('sh')
# districts = ['pudong', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang', 'jiading', 'huangpu', 'jingan', 'zhabei', 'hongkou', 'qingpu', 'fengxian', 'jinshan', 'chongming', 'shanghaizhoubian']
districts = ['pudong', 'minhang', 'baoshan', 'xuhui', 'putuo', 'yangpu', 'changning', 'songjiang', 'huangpu', 'jingan',
             'zhabei', 'hongkou']


def get_community_id_list(city):
    query = models.Community.select().where(models.Community.city == city)
    res = []
    for community in query:
        res.append(community.id)
    return res


def get_chengjiao_id_list():
    query = models.SoldHouseInfo.select()
    res = []
    for house in query:
        res.append(house.houseID)
    return res


def get_ershou_id_list():
    query = models.SellHouseinfo.select()
    res = []
    for house in query:
        res.append(house.houseID)
    return res


# areas = []
# for district in districts:
#     areas.extend(get_areas(city, district))

models.database_init()
# get_community_list(areas=areas)

communities = get_community_id_list(city)
print(len(communities))

# get_community_info(communities=communities, parser=None, pipeline=None)

# get_chengjiao_by_community(communities=communities)
get_ershoufang_by_community(communities=communities)

# house_id = get_chengjiao_id_list()
# print(len(house_id), house_id[:10])
# get_chengjiao_house_info(houses=house_id)
#
# house_id = get_ershou_id_list()
# print(len(house_id), house_id[:10])
# get_ershou_house_info(houses=house_id)


# get_community_info()
