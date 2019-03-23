from scrapy import FormRequest, Request, Spider
from scrapy.conf import settings
from letras.items import Musica
import pymongo


class MusicasSpider(Spider):
    name = "fromalbums"
    baseurl = "https://www.letras.mus.br/"
    start_urls = [
        "https://www.letras.mus.br/"
    ]

    def __init__(self):
        self.db = pymongo.MongoClient(settings["MONGO_URI"])
        self.albums = self.db.letras_dataset.albums.find()

    def get_song(self, response):
        song = {
            "album_id": response.meta["item"]["_id"],
            "ano": response.meta["item"]["info"],
            "artista": response.meta["item"]["artista"],
            "titulo": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h1//text()").get(),
            "letra": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[2]/div[1]/p//text()").getall(),
            "compositor": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[4]/div[1]/text()").get()
        }
        yield Musica(song)
                    
    def parse(self, response):
        
        