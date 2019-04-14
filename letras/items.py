# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Musica(Item):
    genero = Field()
    artista = Field()
    album = Field()
    ano = Field()
    titulo = Field()
    letra = Field()
    compositor = Field()
    link = Field()

class SambaEnredoItem(Item):
    titulo = Field()
    artista_nome = Field()
    letra = Field()
    compositor = Field()