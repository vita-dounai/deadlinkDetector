import scrapy

from deadlinkDetector.items import DeadlinkdetectorItem
from scrapy.http import Request
from urllib.parse import urljoin


class DocSpider(scrapy.Spider):
    name = 'doc_spider'
    allowed_domains = ['fisco-bcos-documentation.readthedocs.io']
    start_urls = [
        'https://fisco-bcos-documentation.readthedocs.io/zh_CN/latest/',
        'https://fisco-bcos-documentation.readthedocs.io/en/latest/docs/introduction.html']
    handle_httpstatus_list = []
    handle_httpstatus_list.extend(range(300, 308))  # 重定向
    handle_httpstatus_list.extend(range(400, 418))  # 客户端错误
    handle_httpstatus_list.extend(range(500, 506))  # 服务器错误

    url_map = {}

    def parse(self, response):
        if response.status == 404:
            if response.url.endswith('/'):
                return None
            print('\033[1;31m' + response.url + '\033[0m', 'FROM',
                  '\033[1;32m' + self.url_map[response.url] + '\033[0m')
            return None
        for link in response.xpath('//a/@href').extract():
            link = urljoin(response.url, link)
            self.url_map[link] = response.url
            yield Request(url=link, callback=self.parse)
