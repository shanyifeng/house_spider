#!/usr/bin/env python
# coding=utf-8

import logging
from bs4 import BeautifulSoup
from lib.spider.common import get_content_of_url

district_map = dict()


def get_district_of_city(city):
    """获取城市行政区划列表

    :param city:  city: 城市首字母,例如 上海：sh
    :return: 小区拼音列表
    """
    result = district_map.get(city)
    if result is None:
        result = do_get_district_of_city(city)
        district_map[city] = result
    return result


def do_get_district_of_city(city):
    """请求城市行政区划列表

    :param city: 城市首字母,例如 上海：sh
    :return: 小区拼音列表
    """

    url = f"http://{city}.lianjia.com/xiaoqu"
    content = get_content_of_url(url)
    soup = BeautifulSoup(content, 'lxml')

    parent_div = soup.find("div", {"data-role": "ershoufang"})
    a_list = parent_div.find_all("a")

    district_list = [a.attrs["href"].replace("/xiaoqu/", "")[:-1]
                     for a in a_list
                     if a.attrs['href'].startswith("/xiaoqu")]
    logging.info(f"{city} 总共 { len(district_list)} 个行政区域")
    return district_list


if __name__ == '__main__':
    districts = get_district_of_city('sh')
    print(districts)
