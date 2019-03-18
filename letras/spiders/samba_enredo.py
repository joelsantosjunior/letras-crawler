from scrapy import Spider, Request
from letras.items import SambaEnredoItem
from scrapy.shell import inspect_response

class classname(Spider):
    name = "sambaenredo"
    baseurl = "https://www.letras.mus.br"
    start_urls = ["http://localhost:8000/samba-enredo.html"]

    def get_song(self, response):
        song = {
            "titulo": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h1//text()").get(),
            "artista_nome": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h2/a//text()").get(),
            "letra": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[2]/div[1]/p//text()").getall(),
            "compositor": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[4]/div[1]/text()").getall(),
        }
        yield SambaEnredoItem(song)

    def song_list(self, response):
        songs = response.css("div.cnt-list--alp")
        for song in songs.css("ul.cnt-list > li"):
            song_link = song.css("a::attr(href)").get()
            yield Request(self.baseurl + song_link, callback=self.get_song)


    def parse(self, response):
        # inspect_response(response, self)
        links = response.css("li > a::attr(href)")
        links = [{
            "link": item.xpath("@href").get(),
            "artist": item.css("a::text").get(),
        } for item in response.xpath("//li//a")]

        for item in links:
            req = Request(self.baseurl + item["link"], callback=self.song_list)
            req.meta["item"] = item
            yield req
