# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from letras.items import Genero, Artista, Album, Musica, SambaEnredoItem
from scrapy.exceptions import DropItem
import json
import pymongo


class MongoPipeline(object):

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'letas_dataset')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Artista):
            instance = self.db.artistas.find_one({"nome": item["nome"]})
            if not instance:
                self.db['artistas'].insert_one(dict(item))
        if isinstance(item, Genero):
            instance = self.db.generos.find_one({"nome": item["nome"]}) 
            if not instance:
                self.db['generos'].insert_one(dict(item))
        if isinstance(item, Album):
            instance = self.db.albums.find_one({"nome": item["nome"], "info": item["info"]}) 
            if not instance:
                self.db['albums'].insert_one(dict(item))
        if isinstance(item, Musica):
            instance = self.db.musicas.find_one({"titulo": item["titulo"], "compositor": item["compositor"]}) 
            if not instance:
                self.db['musicas'].insert_one(dict(item))
        if isinstance(item, SambaEnredoItem):
            instance = self.db.sambaenredo.find_one({"titulo": item["titulo"]})
            if not instance:
                self.db['sambaenredo'].insert_one(dict(item))
        return item

