#!/usr/bin/env python
# coding=utf-8

import logging
from bs4 import BeautifulSoup
from lib.spider.lianjia.common import get_content_of_url

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

    url = f"http://{city}.lianjia.com/xiaoqu/{district}"
    content = get_content_of_url(url)
    soup = BeautifulSoup(content, 'lxml')
    parent_div = soup.find("div", {"data-role": "ershoufang"})
    a_list = parent_div.select('div:nth-of-type(2) a')

    # chinese_area_list = [a.text for a in a_list
    #                      if a.attrs['href'].startswith("/xiaoqu")]
    area_list = [a.attrs["href"].replace("/xiaoqu/", "")[:-1]
                 for a in a_list
                 if a.attrs['href'].startswith("/xiaoqu")]
    logging.info(f"{city}/{district} 总共 {len(area_list)}个商区")
    return area_list


if __name__ == "__main__":
    print(get_areas("sh", "huangpu"))
