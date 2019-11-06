#!/usr/bin/env python
# coding=utf-8
# author:
import logging
from typing import Callable
from lib.spider.lianjia.common import check_block, get_total_pages, get_content_of_request
from lib.spider.scheduler import Scheduler, Request


def start_page_request(city: str, key: str, fmt_url: Callable, parser: Callable):
    """ 分页请求数据

    :param city: 城市
    :param key: URL格式化参数
    :param fmt_url: URL格式化函数
    :param parser: 页面解析函数
    :return:
    """

    def parser_pg2(req: Request, content: str):
        if check_block(content):
            return None

        logging.debug(f"{req.url}")
        return parser(content, city, key) if parser else None

    def parser_pg1(req: Request, content: str):
        if check_block(content):
            return None

        total_pages = get_total_pages(content)
        logging.info(f"{key} total_page {total_pages}")

        results = parser(content, city, key) if parser else content
        requests = [Request(fmt_url(city, key, page), parser_pg2) for page in range(2, total_pages + 1)]

        return results + requests if results else None

    return Request(fmt_url(city, key, 1), parser_pg1)


def scheduler_get_paging(city: str, keys: [], fmt_url: Callable, parser: Callable, pipeline: Callable):
    """请求一批分页数据

    :param city: 城市首字母,例如上海：sh
    :param keys:  URL格式化参数
    :param fmt_url:  URL格式化函数
    :param parser:  页面解析函数
    :param pipeline: 数据处理函数
    :return:
    """

    scheduler = Scheduler(pipeline, fetcher=get_content_of_request)
    reqs = [start_page_request(city, key, fmt_url, parser) for key in keys]
    scheduler.start(reqs)


def scheduler_get_page(city: str, keys: [], fmt_url: Callable, parser: Callable, pipeline: Callable):
    """请求一批详情数据

    :param city: 城市首字母,例如上海：sh
    :param keys:  URL格式化参数
    :param fmt_url:  URL格式化函数
    :param parser:  页面解析函数
    :param pipeline: 数据处理函数
    :return:
    """
    scheduler = Scheduler(pipeline, fetcher=get_content_of_request)
    reqs = [Request(fmt_url(city, key), parser) for key in keys]
    scheduler.start(reqs)
