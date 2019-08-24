#!/usr/bin/env python
# coding=utf-8
# author:
from gevent import monkey

from lib.spider.fang.crawl_area import get_areas
from lib.spider.fang.crawl_district import get_district_of_city
from lib.utility.export import export_table


import logging
from lib import models, path


log_format = '%(asctime)s %(name)s[%(module)s] %(levelname)s: %(message)s'
# logging.basicConfig(format=log_format, level=logging.INFO, handlers=[])
logging.basicConfig(level=logging.DEBUG,
                    format=log_format,
                    handlers=[logging.FileHandler(path.DATA_PATH + "/log.txt"),
                              logging.StreamHandler()])
print(path.ROOT_PATH)

city = 'sh'
# districts = get_district_of_city('sh')
# print(districts)
# [('house-a025', '浦东'), ('house-a029', '嘉定'), ('house-a030', '宝山'), ('house-a018', '闵行'), ('house-a0586', '松江'), ('house-a028', '普陀'), ('house-a021', '静安'), ('house-a024', '黄浦'), ('house-a023', '虹口'), ('house-a031', '青浦'), ('house-a032', '奉贤'), ('house-a035', '金山'), ('house-a026', '杨浦'), ('house-a019', '徐汇'), ('house-a020', '长宁'), ('house-a0996', '崇明'), ('house-a01046', '上海周边')]
districts = ['house-a025', 'house-a018', 'house-a030','house-a019','house-a028','house-a026','house-a020','house-a0586','house-a024','house-a021','house-a023']
areas = []
for district in districts:
    areas.extend(get_areas(city, district))
print(len(areas))


# def get_community_id_list(city):
#     query = models.Community.select().where(models.Community.city == city)
#     res = []
#     for community in query:
#         res.append(community.id)
#     return res
#
#
# def get_chengjiao_id_list():
#     query = models.SoldHouseInfo.select()
#     res = []
#     for house in query:
#         res.append(house.houseID)
#     return res
#
#
# def get_ershou_id_list():
#     query = models.SellHouseinfo.select()
#     res = []
#     for house in query:
#         res.append(house.houseID)
#     return res
#
#
# # areas = []
# # for district in districts:
# #     areas.extend(get_areas(city, district))
#
# # models.database_init()
# # get_community_list(areas=areas)
#
# communities = get_community_id_list(city)
# # print(len(communities))
#
# # get_community_info(communities=communities, parser=None, pipeline=None)
#
# get_chengjiao_by_community(communities=communities)
# # get_ershoufang_by_community(communities=communities)
#
# # house_id = get_chengjiao_id_list()
# # print(len(house_id), house_id[:10])
# # get_chengjiao_house_info(houses=house_id)
# #
# # house_id = get_ershou_id_list()
# # print(len(house_id), house_id[:10])
# # get_ershou_house_info(houses=house_id)
#
#
# # get_community_info()
#
# export_table('sellhouseinfo')