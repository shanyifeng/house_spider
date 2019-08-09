#!/usr/bin/env python
# coding=utf-8
# author:
from lib import models
from lib.spider.lianjia.common import parse_community_list_page, parse_sold_community_page, \
    parse_sell_community_page, parse_rent_community_page, parse_community_info_page
from lib.spider.lianjia.crawl_pages import scheduler_get_paging, scheduler_get_page
from lib.spider.scheduler import Response


def fmt_community_list_url(city, area, page):
    return f"https://{city}.lianjia.com/xiaoqu/{area}/pg{page}/"


def pipeline_community_list(resp: Response):
    with models.database.atomic():
        models.Community.insert_many(resp.result).on_conflict_replace().execute()


def get_community_list(city='sh', areas=['zhangjiang'], parser=parse_community_list_page, pipeline=pipeline_community_list):
    scheduler_get_paging(city, areas, fmt_community_list_url, parser, pipeline)


def fmt_chengjiao_url(city, community, page):
    return f"https://{city}.lianjia.com/chengjiao/c{community}/pg{page}/"


def pipeline_chengjiao(resp: Response):
    with models.database.atomic():
        models.SoldHouseInfo.insert_many(resp.result).on_conflict_replace().execute()


def get_chengjiao_by_community(city='sh', communities=['5011000011756'], parser=parse_sold_community_page,
                               pipeline=pipeline_chengjiao):
    scheduler_get_paging(city, communities, fmt_chengjiao_url, parser, pipeline)


def fmt_ershoufang_url(city, community, page):
    return f"https://{city}.lianjia.com/ershoufang/c{community}/pg{page}/"


def pipeline_ershoufang(resp: Response):
    with models.database.atomic():
        models.SellHouseinfo.insert_many(resp.result).on_conflict_replace().execute()


def get_ershoufang_by_community(city='sh', communities=['5011000011756'], parser=parse_sell_community_page,
                                pipeline=pipeline_ershoufang):
    scheduler_get_paging(city, communities, fmt_ershoufang_url, parser, pipeline)


def fmt_zufang_url(city, community, page):
    return f"https://{city}.lianjia.com/zufang/c{community}/pg{page}/"


def pipeline_zufang(resp: Response):
    with models.database.atomic():
        models.Rentinfo.insert_many(resp.result).on_conflict_replace().execute()


def get_zufang_by_community(city='sh', communities=['5011000011756'], parser=parse_rent_community_page,
                            pipeline=pipeline_zufang):
    scheduler_get_paging(city, communities, fmt_ershoufang_url, parser, pipeline)


def fmt_community_info_url(city, community):
    return f"https://{city}.lianjia.com/xiaoqu/{community}/"


def pipeline_community_info(resp: Response):
    pass


def get_community_info(city='sh', communities=['5011000011756'], parser=parse_community_info_page,
                       pipeline=pipeline_community_info):
    scheduler_get_page(city, communities, fmt_community_info_url, parser, pipeline)


def fmt_ershou_house_info_url(city, house_id):
    return f"https://{city}.lianjia.com/ershoufang/{house_id}.html"


def pipeline_ershou_house_info(resp: Response):
    pass


def get_ershou_house_info(city='sh', houses=['5011000011756'], parser=None, pipeline=None):
    scheduler_get_page(city, houses, fmt_ershou_house_info_url, parser, pipeline)


def fmt_chengjiao_house_info_url(city, house_id):
    return f"https://{city}.lianjia.com/chengjiao/{house_id}.html"


def pipeline_chengjiao_house_info(resp: Response):
    pass


def get_chengjiao_house_info(city='sh', houses=['5011000011756'], parser=None, pipeline=None):
    scheduler_get_page(city, houses, fmt_chengjiao_house_info_url, parser, pipeline)
