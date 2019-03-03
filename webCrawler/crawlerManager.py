from webCrawler.crawler import Crawler
from urllib.parse import urlparse
from queue import Queue
import threading


class CrawlerManager:
    number_of_threads = 1
    max_allowed_thread = 64

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
        self.end_program = False
        self.lock_threads = True
        for _ in range(self.number_of_levels):
            self.lock_all_threads()
            self.check_if_more_threads_required()
            self.move_wait_que_to_que()
            self.unlock_all_threads()
            self.wait_for_all_thread_to_idle()
        self.end_program = True
        self.wait_for_threads_to_close()


############################### thread Helpers #####################################

    def wait_for_threads_to_close(self):
        flag = True
        while flag:
            flag = False
            for thread_entry in self.threadList:
                t = thread_entry['thread']
                if t in threading.enumerate():
                    flag = True
        return

    def wait_for_all_thread_to_idle(self):
        print('Start of the waiting for idle')
        flag = True
        while flag:
            flag = False
            for thread_entry in self.threadList:
                idle = thread_entry['idle']
                if not idle:
                    flag = True
        print('END of the waiting for idle')
        return

    def move_wait_que_to_que(self):
        for q in self.waiting_queue:
                self.queue.put(q)
        self.waiting_queue = set()

    def create_threads(self, n):
        for _ in range(n):
            t = threading.Thread(target=self.work, daemon=True)
            t.start()
            self.threadList.append({'thread': t, 'idle': True})

    def work(self):
        while not self.end_program:
            if not self.lock_threads and self.queue.qsize():
                self.activate_thread()
                url = self.queue.get()
                self.run_crawler(url)
                self.queue.task_done()
            else:
                self.make_thread_idle()

    def make_thread_idle(self):
        for i, thread_entry in enumerate(self.threadList):
            t = thread_entry['thread']
            if t == threading.current_thread():
                self.threadList[i]['idle'] = True

    def activate_thread(self):
        for i, thread_entry in enumerate(self.threadList):
            t = thread_entry['thread']
            if t == threading.current_thread():
                self.threadList[i]['idle'] = False

    def lock_all_threads(self):
        self.lock_threads = True

    def unlock_all_threads(self):
        self.lock_threads = False

    # Todo Need to aadd logic to control the number of threads required based on the wating list
    def check_if_more_threads_required(self):
        if len(self.waiting_queue) < CrawlerManager.max_allowed_thread:
            self.number_of_threads = len(self.waiting_queue)
            if len(self.threadList) < self.number_of_threads:
                self.create_threads(self.number_of_threads - len(self.threadList))
        return

    def print_thread_list(self):
        for t in self.threadList:
            print(t)
        print("###########################################################################")
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
