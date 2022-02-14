# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import scrapy

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline


class SiteparserPipeline:
    def __init__(self):
        client = MongoClient("127.0.0.1", 27017)
        self.mongobase = client.lm

    def process_item(self, item, spider):
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item


class SiteImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for img in item["photos"]:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item["photos"] = [itm[1] for itm in results if itm[0]]
        return item
