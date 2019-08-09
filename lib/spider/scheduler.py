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


class FuncWrapper:
    """封装任务参数"""

    def __init__(self, fn, *args, **kwargs):
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    def __call__(self):
        return self.fn(*self.args, **self.kwargs)

    def __str__(self):
        return f"fn:{self.fn.__name__}, args:{self.args}, kwargs:{self.kwargs}"


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

    def __init__(self, pipeline, fetcher=None, max_running=5):
        self.pipeline = pipeline
        self.tasks = gevent.queue.Queue(-1)
        self.max_running = max_running
        self.fetcher = fetcher or default_fetcher
        self.working = 0

    def start(self, reqs):
        """开始并发请求
        :param reqs: 请求
        :return:
        """
        for req in reqs:
            self.add_task(self.worker_fetch, req)

        threads = [gevent.spawn(self.worker, i)
                   for i in range(self.max_running)]
        gevent.joinall(threads)

    def worker(self, n):
        """工作函数，调用真正的函数
        :param n: 编号
        :return: None
        """
        while self.working > 0 or not self.tasks.empty():
            t1 = time.time()  # 开始计时
            logger.debug(f"worker {n} begin {t1} , {self.working} {self.tasks.empty()}")
            try:
                self.tasks.get(timeout=5)()
                self.working -= 1
            except gevent.queue.Empty:
                gevent.sleep(0)
            except:
                self.working -= 1
                import traceback
                traceback.print_exc()
            gevent.sleep(0)
            logger.debug(f"worker {n} cost {time.time() - t1}")
        logger.info(f'worker {n} end')

    def add_task(self, fun, *args, **kwargs):
        """封装任务，添加到任务队列
        :param fun: 执行的函数
        :param args: 参数
        :param kwargs: 参数
        :return: None
        """
        logger.debug(f"add_task {fun.__name__}")
        self.working += 1
        self.tasks.put(FuncWrapper(fun, *args, **kwargs))

    def worker_fetch(self, req):
        """请求网页并添加解析任务
        :param req: 请求
        :return:
        """
        data = self.fetcher(req)
        self.add_task(self.worker_parser, req, data)

    def worker_parser(self, req, data):
        """解析并添加pipeline或fetch任务
        :param req:
        :param data:
        :return:
        """
        if not data:
            return

        results = []
        requests = []
        if req.parser:
            res, requests = req.parser(req, data)
            if res:
                results += res
        else:
            results.append(data)

        if self.pipeline:
            r = Response(request=req, result=results)
            self.add_task(self.pipeline, r)

        if requests:
            for request in requests:
                self.add_task(self.worker_fetch, request)


if __name__ == "__main__":
    pass
