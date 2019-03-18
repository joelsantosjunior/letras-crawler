from scrapy import FormRequest, Request, Spider
from scrapy.conf import settings
from letras.items import SongItem
import pymongo


class MusicasSpider(Spider):
    name = "musicasspy"
    baseurl = "https://www.letras.mus.br/"
    start_urls = [
        "https://www.letras.mus.br/"
    ]

    def __init__(self):
        self.db = pymongo.MongoClient(settings["MONGO_URI"])
        self.albums = self.db.letras_dataset.albums.find()

    def get_song(self, response):
        song = {
            "album_id": response.meta["item"]["album"],
            "titulo": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h1//text()").get(),
            "artista_nome": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h2/a//text()").get(),
            "letra": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[2]/div[1]/p//text()").getall(),
            "compositor": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[4]/div[1]/text()").get(),
            "ano": response.meta["item"]["info"]
        }
        yield SongItem(song)
                    
    def parse(self, response):
        for album in self.albums:
            songs = album["songs"]
            if len(songs) > 0:
                for song in songs:
                    req = Request(self.baseurl + song["link"][1:], callback=self.get_song)
                    req.meta["item"] = {"album": album["_id"], "info": album["info"]}
                    yield req