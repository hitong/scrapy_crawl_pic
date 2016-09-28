# -*- coding: UTF-8 -*-
import scrapy
from scrapy.spider import BaseSpider
from mmpic.items import Mm131Item
import sys

reload(sys)
sys.setdefaultencoding("utf-8")


def get_6_url():
    urls = []
    for i in range(1, 79):
        urls.append("http://www.mm131.com/xinggan/list_6_" + str(i) + ".html")
    return urls


def get_1_url():
    urls = []
    for i in range(1, 31):
        urls.append("http://www.mm131.com/qingchun/list_1_" + str(i) + ".html")
    return urls


class Mm131Spider(BaseSpider):
    name = "mm131"
    allowed_domains = ['mm131.com']
    start_urls = []  # "http://www.mm131.com/xinggan/2681.html"

    start_urls.extend(get_1_url())
    start_urls.extend(get_6_url())

    # img1/mm131.com/pic/
    def parse(self, response):
        detail_urls = response.xpath('//dd/a[@target="_blank"]/@href').extract()
        for detail_url in detail_urls:
            if "baidu" in detail_url:
                continue
            print detail_url
            yield scrapy.Request(detail_url, callback=self.parse_detail)

    def parse_detail(self, response):
        place_url = response.xpath('//div[@class="place"]/a/@href').extract()[1]
        num_text = response.xpath('//span[@class="page-ch"]/text()').extract()[0]
        first_url = response.xpath('//div[@class="content-pic"]/a/img/@src').extract()[0]
        place = place_url.split('/')[-2]
        print num_text
        num = get_num(num_text)
        # print "0000000000" + str(num)
        item = Mm131Item()
        item['place'] = place
        item['image_urls'] = get_urls(first_url, num)
        yield item


def get_num(num_txt):
    return num_txt.replace("共", "").replace("页", "")


# 根据URL和页数拼出所有连接
def get_urls(url, num):
    image_urls = []
    last_str = url.split('/')[-1]
    head = url.replace(last_str, "")
    for i in range(1, int(num) + 1):
        img_url = head + str(i) + ".jpg"
        image_urls.append(img_url)
    return image_urls
