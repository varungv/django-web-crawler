from urllib import request
from urllib.error import URLError
from webCrawler.MyHtmlParser import MyHtmlParser


class Crawler:

    def __init__(self, base_url, path_name):
        self.path_name = path_name
        self.base_url = base_url
        self.http_protocol = path_name.split('/')[0][:-1]  # to get http or https

    def crawl(self):
        link_collection = {
                    "links": set(),
                    "image_links": set()
                }
        msg = ''
        try:
            res = request.urlopen(self.path_name)
            if 'text/html' in res.getheader('Content-Type'):
                parser = MyHtmlParser(self.base_url, self.http_protocol)
                parser.feed(res.read().decode('utf-8'))
                link_collection = {
                    "links": parser.get_links(),
                    "image_links": parser.get_image_links()
                }
        except Exception as e:
            msg = 'Not all the links were fetchable as the crawling website has blocked oue request!'

        return link_collection, msg
