#!/usr/bin/env python
# coding=utf-8
# author:
import random

from bs4 import BeautifulSoup
import requests

headers = dict()
headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0'
headers["Host"] = 'www.xicidaili.com'


def crawl_proxies():
    proxies = []
    try:
        url = 'http://www.xicidaili.com/nt/1'
        req = requests.get(url, headers=headers)
        source_code = req.content
        soup = BeautifulSoup(source_code, 'lxml')
        ips = soup.findAll('tr')

        for x in range(1, len(ips)):
            ip = ips[x]
            tds = ip.findAll("td")
            proxy_host = "{0}://".format(tds[5].contents[0]) + tds[1].contents[0] + ":" + tds[2].contents[0]
            proxy_temp = {tds[5].contents[0], proxy_host}
            proxies.append(proxy_temp)
    except Exception as e:
        print("spider_proxyip exception:")
        print(e)
    http = [v for k, v in proxies if k == 'HTTP']
    https = [v for k, v in proxies if k == 'HTTPS']
    return http, https


http_proxy, https_proxy = crawl_proxies()


def get_proxies():
    global http_proxy, https_proxy

    while not (http_proxy and https_proxy):
        http_proxy, https_proxy = crawl_proxies()

    proxies = {
        "http": random.choice(http_proxy),
        "https": random.choice(https_proxy),
    }
    return proxies


if __name__ == '__main__':
    # proxies = crawl_proxies()
    # http_proxy = [(k, v) for k, v in proxies if k == 'HTTP']
    # print(http_proxy)
    print(get_proxies())
