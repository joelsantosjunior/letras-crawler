# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LetrasItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GenreItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

class ArtistItem(scrapy.Item):
    artist_name = scrapy.Field()
    artist_url = scrapy.Field()
    artist_image = scrapy.Field()
    artist_genre = scrapy.Field()

class AlbumItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    image = scrapy.Field()
    info = scrapy.Field()
    songs = scrapy.Field()