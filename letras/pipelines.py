# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from letras.items import GenreItem, ArtistItem, AlbumItem, SongItem, SambaEnredoItem
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
        if isinstance(item, ArtistItem):
            instance = self.db.artistas.find_one({"artist_name": item["artist_name"]})
            if not instance:
                self.db['artistas'].insert_one(dict(item))
        if isinstance(item, GenreItem):
            instance = self.db.generos.find_one({"name": item["name"]}) 
            if not instance:
                self.db['generos'].insert_one(dict(item))
        if isinstance(item, AlbumItem):
            instance = self.db.albums.find_one({"name": item["name"], "info": item["info"]}) 
            if not instance:
                self.db['albums'].insert_one(dict(item))
        if isinstance(item, SongItem):
            instance = self.db.musicas.find_one({"titulo": item["titulo"], "album_id": item["album_id"]}) 
            if not instance:
                self.db['musicas'].insert_one(dict(item))
        if isinstance(item, SambaEnredoItem):
            instance = self.db.sambaenredo.find_one({"titulo": item["titulo"]}) 
            if not instance:
                self.db['sambaenredo'].insert_one(dict(item))
        return item


class CheckForDuplication(object):
    def __init__(self):
        self.artists = set()
        self.genres = set()
        self.songs = set()
        self.sambas = set()

    def process_item(self, item, spider):
        if not isinstance(item, ArtistItem) or \
            not isinstance(item, AlbumItem) or \
            not isinstance(item, SongItem) or \
            not isinstance(item, SambaEnredoItem) or \
            not isinstance(item, GenreItem):
            return item

        if isinstance(item, GenreItem):
            if item['name'] in self.genres:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.genres.add(item['name'])

        if isinstance(item, ArtistItem):
            if item['artist_name'] in self.artists:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.artists.add(item['artist_name'])

        if isinstance(item, SambaEnredoItem):
            if item['titulo'] in self.sambas:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.sambas.add(item['titulo'])

        if isinstance(item, SongItem):
            song_info = item['album_id'] + item["titulo"]
            if song_info in self.songs:
                raise DropItem("Duplicate item found: %s" % item)
            else:
                self.genres.add(song_info)