#!/usr/bin/env python
# coding=utf-8

import logging
from bs4 import BeautifulSoup, SoupStrainer
from lib.spider.common import get_content_of_url
from lib.spider.fang.common import create_headers

area_map = dict()


def get_areas(city='sh', district='pudong'):
    """
    通过城市和区县名获得下级板块名
    :param city: 城市
    :param district: 区县
    :return: 区县列表
    """
    key = f'{city}/{district}'
    result = area_map.get(key)
    if result is None:
        result = do_get_areas(city, district)
        area_map[key] = result
    return result


def do_get_areas(city, district):
    """
    通过城市和区县名获得下级板块名
    :param city: 城市
    :param district: 区县
    :return: 区县列表
    """

    url = f"https://{city}.esf.fang.com/{district}/"
    content = get_content_of_url(url, headers=create_headers())
    soup = BeautifulSoup(content, 'lxml',  from_encoding="gb18030", parse_only=SoupStrainer("div", {"id": "ri010"}))
    a_list = soup.select("li.area_sq li a")
    area_list = [(a.attrs["href"][1:-1], a.text) for a in a_list]
    logging.info(f"{city} 总共 { len(area_list)} 个商区")
    return area_list


if __name__ == "__main__":
    print(get_areas("sh", "house-a025"))
