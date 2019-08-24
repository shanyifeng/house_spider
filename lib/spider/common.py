#!/usr/bin/env python
# coding=utf-8
# author:
import logging
import os
import time
import requests
from urllib.request import url2pathname
from lib.path import DATA_PATH
from settings import USE_CACHE, SVAE_CACHE


def url_path(url: str):
    """ url转位path

    :param url:
    :return:
    """
    if url.startswith('http://'):
        # logging.debug("startswith http")
        url = url.replace('http://', '')
    elif url.startswith('https://'):
        # logging.debug("startswith https")
        url = url.replace('https://', '')
    if url.endswith('/'):
        url = url[:-1]
    if not url.endswith('.html'):
        url += '.html'
    url = os.path.join(DATA_PATH, url)
    # logging.debug("url %s", url)
    return url2pathname(url)


def save_page(path: str, content: str):
    """保存网页内容到文件

    :param path: 存储的文件
    :param content: 存储的内容
    :return:
    """
    # logging.debug("path %s", path)
    parent = os.path.dirname(path)
    if not os.path.exists(parent):
        os.makedirs(parent)
    with open(path, 'wb') as f:
        f.write(content)


def get_content_of_url(url: str, params=None, **kwargs) -> str:
    """
    :param url: URL for the new :class:`Request` object.
    :param params: (optional) Dictionary, list of tuples or bytes to send
        in the query string for the :class:`Request`.
    :param \*\*kwargs: Optional arguments that ``request`` takes.
    :return: :class:`Response <Response>` object
    :rtype: requests.Response
    """
    logging.debug("fetch_page %s", url)
    path = url_path(url)
    content = None
    if USE_CACHE and os.path.exists(path):
        with open(path, 'rb') as f:
            content = f.read()

    if content:
        logging.debug("use cache url %s", url)
    else:
        r = requests.get(url, params=params, **kwargs)
        if not r.ok:
            logging.error("requests ok: %d url %s", r.status_code, url)
        else:
            content = r.content
            logging.debug("requests ok: %d url %s", r.status_code, url)

        if SVAE_CACHE:
            save_page(path, content)

    return content
