# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field

class Genero(Item):
    nome = Field()
    link = Field()

class Artista(Item):
    nome = Field()
    link = Field()
    genero = Field()

class Album(Item):
    nome = Field()
    link = Field()
    info = Field()
    musicas = Field()
    artista = Field()

class Musica(Item):
    album_id = Field()
    titulo = Field()
    artista = Field()
    letra = Field()
    compositor = Field()
    ano = Field()

class SambaEnredoItem(Item):
    titulo = Field()
    artista_nome = Field()
    letra = Field()
    compositor = Field()