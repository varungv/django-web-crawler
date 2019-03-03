from webCrawler.crawler import Crawler
from urllib.parse import urlparse
from queue import Queue
import threading


class CrawlerManager:
    number_of_threads = 8

    def __init__(self, url, number_of_levels):
        self.url = url
        self.base_url = urlparse(url).netloc
        self.number_of_levels = number_of_levels
        self.queue = Queue()
        self.waiting_queue = set()
        self.crawled = set()
        self.image_links = set()
        self.msg = ''
        self.threadList = []
        self.waiting_queue.add(url)
        for _ in range(self.number_of_levels):
            self.move_wait_que_to_que()
            self.create_threads()
            self.wait_for_threads_to_close()


############################### thread Helpers #####################################

    def wait_for_threads_to_close(self):
        flag = True
        while flag:
            flag = False
            for t in self.threadList:
                if t in threading.enumerate():
                    flag = True
        return

    def move_wait_que_to_que(self):
        for q in self.waiting_queue:
                self.queue.put(q)
        self.waiting_queue = set()

    def create_threads(self):
        for _ in range(CrawlerManager.number_of_threads):
            t = threading.Thread(target=self.work)
            t.start()
            self.threadList.append(t)

    def work(self):
        while self.queue.qsize():
            url = self.queue.get()
            self.run_crawler(url)
            self.queue.task_done()

############################### thread Helpers #####################################

    def run_crawler(self, path):
        crawler = Crawler(self.base_url, path)
        link_collection, msg = crawler.crawl()
        self.crawled.add(path)
        self.msg = msg
        for link in link_collection['links']:
            if link not in self.crawled:
                self.waiting_queue.add(link)

        for link in link_collection['image_links']:
            self.image_links.add(link)

        return

    def get_links(self):
        res = set()
        for link in self.crawled:
            res.add(link)

        for link in self.waiting_queue:
            res.add(link)

        return res

    def get_images_links(self):
        return self.image_links

    def __len__(self):
        return len(self.crawled) + len(self.image_links)

    def __str__(self):
        return str({
            "waiting_que": list(self.waiting_queue),
            "crawled": list(self.crawled)
        })
