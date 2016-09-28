# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


# url http://img1.mm131.com/pic/2671/0.jpg

def get_urls(url):
    image_urls = [];
    last_str = url.split('/')[-1]
    head = url.replace(last_str, "")
    for i in range(1, 51):
        img_url = head + str(i) + ".jpg"
        image_urls.append(img_url)
    return image_urls


class MmpicPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            last_str = image_url.split('/')[-1]
            head = image_url.replace(last_str, "")
            for i in range(1, 51):
                img_url = head + str(i) + ".jpg"
                print img_url
                yield scrapy.Request(img_url, meta={'place': item['place'], 'hash': hash(img_url)})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

    def file_path(self, request, response=None, info=None):
        place = request.meta['place']
        hash_value = request.meta['hash']
        filename = u'full/{0}/{1}'.format(place, hash_value)
        return filename
