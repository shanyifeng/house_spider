#!/usr/bin/env python
# coding=utf-8

import logging
from bs4 import BeautifulSoup, SoupStrainer
from lib.spider.common import get_content_of_url
from lib.spider.fang.common import create_headers

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

    url = f"https://{city}.esf.fang.com/"
    content = get_content_of_url(url, headers=create_headers)
    soup = BeautifulSoup(content, 'lxml',  from_encoding="gb18030", parse_only=SoupStrainer("div", {"id": "ri010"}))
    a_list = soup.select("#ri010 > div:nth-of-type(1) > ul:nth-of-type(1) > li:nth-of-type(1) li a")
    district_list = [(a.attrs["href"][1:-1], a.text) for a in a_list]
    logging.info(f"{city} 总共 { len(district_list)} 个行政区域")
    return district_list


if __name__ == '__main__':
    districts = get_district_of_city('sh')
    print(districts)
