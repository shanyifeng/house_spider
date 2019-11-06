# -*- coding: utf-8 -*-
import re
import json
import logging
import lib.spider.common
from bs4 import BeautifulSoup, SoupStrainer
from lib.request.headers import choice_ua
from lib.spider.scheduler import Request

site = 'lianjia'


def create_headers():
    headers = dict()
    headers["User-Agent"] = choice_ua()
    return headers


def get_content_of_url(url) -> str:
    """ warp lib.spider.common.get_content_of_url

    :param req:
    :return:
    """
    return lib.spider.common.get_content_of_url(url, headers=create_headers())



def get_content_of_request(req: Request) -> str:
    """ warp lib.spider.common.get_content_of_url

    :param req:
    :return:
    """
    return get_content_of_url(req.url)


def check_block(content: str) -> bool:
    """
    @param content:
    @return:
    """
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('title'))
    if soup.title.string == "414 Request-URI Too Large":
        logging.error(
            "Lianjia block your ip, please verify captcha manually at lianjia.com")
        return True
    return False


def get_total_count(content: str) -> int:
    """ 总数
    :param content: r.content
    :return: count
    """
    total_count = 0
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer("h2", {"class": "total fl"}))
    try:
        total_count = int(soup.find("span").get_text())
    except:
        pass
    return total_count


def get_total_pages(content: str) -> int:
    """ 总页数

    :param content: r.content
    :return: count
    """
    total_pages = 1
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer("div", {"class": "page-box house-lst-page-box"}))
    try:
        total_pages = int(json.loads(soup.find("div").attrs["page-data"])["totalPage"])
    except:
        pass

    return total_pages


def parse_community_info_page(req: Request, content: str) -> []:
    if check_block(content):
        return None

    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer("div", {"class": "xiaoquInfoItem"}))
    communityinfos = soup.findAll("div", {"class": "xiaoquInfoItem"})
    res = {}
    for info in communityinfos:
        key_type = {
            u"建筑年代": u'year',
            u"建筑类型": u'housetype',
            u"物业费用": u'cost',
            u"物业公司": u'service',
            u"开发商": u'company',
            u"楼栋总数": u'building_num',
            u"房屋总数": u'house_num',
        }
        try:
            key = info.find("span", {"xiaoquInfoLabel"})
            value = info.find("span", {"xiaoquInfoContent"})
            key_info = key_type[key.get_text().strip()]
            value_info = value.get_text().strip()
            res.update({key_info: value_info})
        except:
            continue

    return res


def parse_community_list_page(content: str, city: str, community: str):
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'leftContent'}))
    nameList = soup.findAll("li", {"class": "clear"})
    data_source = []
    for name in nameList:  # Per item loop
        info_dict = {}
        try:
            communitytitle = name.find("div", {"class": "title"})
            title = communitytitle.get_text().strip('\n')
            link = communitytitle.a.get('href')
            info_dict.update({u'title': title})
            info_dict.update({u'link': link})

            district = name.find("a", {"class": "district"})
            info_dict.update({u'district': district.get_text()})

            bizcircle = name.find("a", {"class": "bizcircle"})
            info_dict.update({u'bizcircle': bizcircle.get_text()})

            tagList = name.find("div", {"class": "tagList"})
            info_dict.update({u'tagList': tagList.get_text().strip('\n')})

            onsale = name.find("a", {"class": "totalSellCount"})
            info_dict.update(
                {u'onsale': onsale.span.get_text().strip('\n')})

            onrent = name.find("a", {"title": title + u"租房"})
            info_dict.update(
                {u'onrent': onrent.get_text().strip('\n').split(u'套')[0]})

            info_dict.update({u'id': name.get('data-housecode')})

            price = name.find("div", {"class": "totalPrice"})
            info_dict.update({u'price': price.span.get_text().strip('\n')})

            # communityinfo = get_community_info_by_url(link)
            # for key, value in communityinfo:
            #     info_dict.update({key: value})

            info_dict.update({u'city': city})
        except:
            logging.error(f'exception {__name__}')
            continue
        # communityinfo insert into mysql
        data_source.append(info_dict)
    return data_source


def parse_sold_community_page(content: str, city: str, community: str):
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'position'}))
    selected = soup.find("a", {"class":"selected"})
    if selected and selected.get('href') == '/chengjiao/':
        print(selected)
        return None

    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'leftContent'}))
    data_source = []
    ultag = soup.find("ul", {"class": "listContent"})
    if ultag:
        for name in ultag.find_all('li'):
            info_dict = {}
            try:
                housetitle = name.find("div", {"class": "title"})
                info_dict.update({u'title': housetitle.get_text().strip()})
                info_dict.update({u'link': housetitle.a.get('href')})
                houseID = housetitle.a.get(
                    'href').split("/")[-1].split(".")[0]
                info_dict.update({u'houseID': houseID.strip()})
                house = housetitle.get_text().strip().split(' ')
                info_dict.update({u'community': community})
                info_dict.update(
                    {u'housetype': house[1].strip() if 1 < len(house) else ''})
                info_dict.update(
                    {u'square': house[2].strip() if 2 < len(house) else ''})

                houseinfo = name.find("div", {"class": "houseInfo"})
                info = houseinfo.get_text().split('|')
                info_dict.update({u'direction': info[0].strip()})
                info_dict.update(
                    {u'status': info[1].strip() if 1 < len(info) else ''})

                housefloor = name.find("div", {"class": "positionInfo"})
                floor_all = housefloor.get_text().strip().split(' ')
                info_dict.update({u'floor': floor_all[0].strip()})
                info_dict.update({u'years': floor_all[-1].strip()})

                followInfo = name.find("div", {"class": "source"})
                info_dict.update(
                    {u'source': followInfo.get_text().strip()})

                totalPrice = name.find("div", {"class": "totalPrice"})
                if totalPrice.span is None:
                    info_dict.update(
                        {u'totalPrice': totalPrice.get_text().strip()})
                else:
                    info_dict.update(
                        {u'totalPrice': totalPrice.span.get_text().strip()})

                unitPrice = name.find("div", {"class": "unitPrice"})
                if unitPrice.span is None:
                    info_dict.update(
                        {u'unitPrice': unitPrice.get_text().strip()})
                else:
                    info_dict.update(
                        {u'unitPrice': unitPrice.span.get_text().strip()})

                dealDate = name.find("div", {"class": "dealDate"})
                info_dict.update(
                    {u'dealdate': dealDate.get_text().strip().replace('.', '-')})

            except:
                logging.error(f'exception {__name__}')
                continue
            # Sellinfo insert into mysql
            data_source.append(info_dict)
            # model.Sellinfo.insert(**info_dict).upsert().execute()

    if not data_source:
        logging.info(f"empty {community}")
    return data_source


def parse_rent_community_page(content: str, city: str, community: str):
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'leftContent'}))
    data_source = []
    for ultag in soup.findAll("ul", {"class": "house-lst"}):
        for name in ultag.find_all('li'):
            info_dict = {}
            try:
                housetitle = name.find("div", {"class": "info-panel"})
                info_dict.update({u'title': housetitle.get_text().strip()})
                info_dict.update({u'link': housetitle.a.get('href')})
                houseID = housetitle.a.get(
                    'href').split("/")[-1].split(".")[0]
                info_dict.update({u'houseID': houseID})

                region = name.find("span", {"class": "region"})
                info_dict.update({u'region': region.get_text().strip()})

                zone = name.find("span", {"class": "zone"})
                info_dict.update({u'zone': zone.get_text().strip()})

                meters = name.find("span", {"class": "meters"})
                info_dict.update({u'meters': meters.get_text().strip()})

                other = name.find("div", {"class": "con"})
                info_dict.update({u'other': other.get_text().strip()})

                subway = name.find("span", {"class": "fang-subway-ex"})
                if subway is None:
                    info_dict.update({u'subway': ""})
                else:
                    info_dict.update(
                        {u'subway': subway.span.get_text().strip()})

                decoration = name.find("span", {"class": "decoration-ex"})
                if decoration is None:
                    info_dict.update({u'decoration': ""})
                else:
                    info_dict.update(
                        {u'decoration': decoration.span.get_text().strip()})

                heating = name.find("span", {"class": "heating-ex"})
                info_dict.update(
                    {u'heating': heating.span.get_text().strip()})

                price = name.find("div", {"class": "price"})
                info_dict.update(
                    {u'price': int(price.span.get_text().strip())})

                pricepre = name.find("div", {"class": "price-pre"})
                info_dict.update(
                    {u'pricepre': pricepre.get_text().strip()})
            except:
                logging.error(f'exception {__name__}')
                continue
            # Rentinfo insert into mysql
            data_source.append(info_dict)
            # model.Rentinfo.insert(**info_dict).upsert().execute()
    if not data_source:
        logging.info(f"empty {community}")
    return data_source


def parse_sell_community_page(content: str, city: str, community: str):
    soup = BeautifulSoup(content, 'lxml', parse_only=SoupStrainer('div', attrs={'class': 'leftContent'}))
    no_result = soup.find("div", {"class":"m-noresult"})
    logging.info(no_result)
    if no_result:
        return None

    data_source = []
    ultag = soup.find("ul", {"class": "sellListContent"}, recursive=False)
    if ultag:
        for name in ultag.find_all('li'):
            info_dict = {}
            try:
                housetitle = name.find("div", {"class": "title"})
                info_dict.update(
                    {u'title': housetitle.a.get_text().strip()})
                info_dict.update({u'link': housetitle.a.get('href')})
                houseID = housetitle.a.get(
                    'href').split("/")[-1].split(".")[0]
                info_dict.update({u'houseID': houseID.strip()})

                houseinfo = name.find("div", {"class": "houseInfo"})
                if city == 'bj':
                    info = houseinfo.get_text().split('/')
                else:
                    info = houseinfo.get_text().split('|')
                info_dict.update({u'community': community})
                info_dict.update({u'housetype': info[1]})
                info_dict.update({u'square': info[2]})
                info_dict.update({u'direction': info[3]})
                info_dict.update({u'decoration': info[4]})

                positionInfo = name.find("div", {"class": "positionInfo"}).find(text=True)[:-5]
                index = positionInfo.find(')')
                if index >= 0:
                    info_dict.update({u'floor': positionInfo[:index + 1]})
                    info_dict.update({u'years': positionInfo[index + 1:]})
                else:
                    info_dict.update({u'years': positionInfo})
                    info_dict.update({u'floor': positionInfo})

                followInfo = name.find("div", {"class": "followInfo"})
                info_dict.update(
                    {u'followInfo': followInfo.get_text().strip()})

                taxfree = name.find("span", {"class": "taxfree"})
                if taxfree == None:
                    info_dict.update({u"taxtype": ""})
                else:
                    info_dict.update(
                        {u"taxtype": taxfree.get_text().strip()})

                totalPrice = name.find("div", {"class": "totalPrice"})
                info_dict.update(
                    {u'totalPrice': totalPrice.span.get_text()})

                unitPrice = name.find("div", {"class": "unitPrice"})
                info_dict.update(
                    {u'unitPrice': unitPrice.get("data-price")})
            except:
                logging.error(f'exception {__name__}')
                continue
            data_source.append(info_dict)

    if not data_source:
        logging.info(f"empty {community}")
    return data_source
