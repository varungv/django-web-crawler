from html.parser import HTMLParser
from urllib import parse


class MyHtmlParser(HTMLParser):

    def __init__(self, base_url, http_protocol):
        super().__init__()
        self.base_url = base_url
        self.links = set()
        self.image_links = set()
        self.http_protocol = http_protocol

    def error(self, message):
        pass

    def handle_starttag(self, tag, attrbs):
        if tag == 'a' or tag == 'img':
            for (attribute, value) in attrbs:
                if attribute == 'href' or attribute == 'src':
                    url = parse.urljoin(self.base_url, value)
                    if url[:1] == '/':
                        url = self.http_protocol + '://' + self.base_url + url
                    if self.base_url in url and 'http' in url:
                        if url[-1] == '/':
                            url = url[:-1]

                        if tag == 'a':
                            self.links.add(url)
                        else:
                            self.image_links.add(url)

    def get_links(self):
        return self.links

    def get_image_links(self):
        return self.image_links
