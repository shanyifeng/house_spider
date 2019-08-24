# -*- coding: utf-8 -*-
import logging
import time
import gevent
import gevent.queue
from lib.spider.common import get_content_of_url

logger = logging.getLogger(__name__)


def retry_on_url_error(fetcher, try_cnt=3):
    def wrapper(self, *args, **kwargs):
        for i in range(try_cnt):
            try:
                return fetcher(self, *args, **kwargs)
            except Exception as e:
                logger.info("retry %s time(s)" % (i + 1))
                if i == try_cnt - 1:
                    raise e
                time.sleep(1)

    return wrapper


class Request(object):
    def __init__(self, url="", parser=None):
        self.url = url
        self.parser = parser

    def __str__(self):
        return f"Request url {self.url}"

    def __repr__(self):
        return f"Request url {self.url}"


class Response(object):
    def __init__(self, request=None, result=None):
        self.request = request
        self.result = result

    def __str__(self):
        return f"Response req:{self.request} resp:{self.result}"


def default_fetcher(req: Request):
    return get_content_of_url(req.url)


class Scheduler(object):
    """任务调度"""

    def __init__(self, pipeline, fetcher=None, max_running=20):
        self.pipeline = pipeline
        self.tasks = gevent.queue.Queue(-1)
        self.max_running = max_running
        self.fetcher = fetcher or default_fetcher

    def start(self, reqs):
        """开始并发请求
        :param reqs: 请求
        :return:
        """

        self.add_tasks(reqs)
        threads = [gevent.spawn(self.worker, i)
                   for i in range(self.max_running)]
        gevent.joinall(threads)

    def worker(self, n):
        """工作函数，调用真正的函数
        :param n: 编号
        :return: None
        """
        while not self.tasks.empty():
            t1 = time.time()  # 开始计时
            logger.debug(f"worker {n} begin {t1} , {self.tasks.qsize()}")
            try:
                req = self.tasks.get(timeout=3)
                requests = self.spider(req)
                self.add_tasks(requests)
            except gevent.queue.Empty:
                gevent.sleep(0)
            except:
                print(req)
                import traceback
                traceback.print_exc()
            gevent.sleep(0)
            logger.debug(f"worker {n} cost {time.time() - t1}")
        logger.info(f'worker {n} end')

    def add_task(self, req: Request):
        if req:
            self.tasks.put(req)

    def add_tasks(self, reqs):
        if reqs:
            for req in reqs:
                self.add_task(req)

    def spider(self, req):
        """请求网页并添加解析任务
        :param req: 请求
        :return:
        """

        requests = []
        data = self.fetcher(req)
        if data:
            results = []
            if not req.parser:
                results.append(data)
            else:
                res = req.parser(req, data)
                if isinstance(res, list):
                    for r in res:
                        if isinstance(r, Request):
                            requests.append(r)
                        else:
                            results.append(r)
                elif res:
                    results.append(res)

            if self.pipeline and results:
                r = Response(request=req, result=results)
                self.pipeline(r)
        return requests


if __name__ == "__main__":
    pass
