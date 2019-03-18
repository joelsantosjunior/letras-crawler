from scrapy import FormRequest, Request, Spider
from letras.items import GenreItem, ArtistItem, AlbumItem


class LetrasSpider(Spider):
    name = "letrasspy"
    start_urls = [
        'https://www.letras.mus.br/',
    ]

    def song(self, response):
        pass

    def discography(self, response):
        albums = response.css('div.cnt-discografia_cd')
        for album in albums:
            info = album.css("div.cnt-discografia_info")
            album_item = {
                "name": info.css("h4 > a::text").get(),
                "link": info.css("h4 > a::attr(href)").get(),
                "image": info.css("img::attr(src)").get(),
                "info": info.css("span::text").get(),
                "artist": response.meta["item"],
                "songs": [{
                    "link": _.css("a::attr(href)").get(),
                    "title": _.css("a::attr(title)").get()
                } for _ in album.css("ol.cnt-list > li")]
            }
            yield AlbumItem(album_item)

    def artists(self, response):
        artists = response.css('ul.cnt-list-thumb-l > li')

        for artist in artists:
            artist_item = {
                "artist_name": artist.css('a > span > b::text').get(),
                "artist_url": artist.css('a::attr(href)').get(),
                "artist_image": artist.css('a > img::attr(data-original)').get(),
                "artist_genre": response.meta['item']
            }

            # yield ArtistItem(artist_item)
            next_url = self.start_urls[0] + \
                artist_item["artist_url"][1:] + "discografia"
            req = Request(next_url, callback=self.discography)
            req.meta["item"] = artist_item["artist_name"]
            yield req

    def parse(self, response):
        all_genres = response.css('.js-tab-link')

        for genre in all_genres:
            item = GenreItem()
            item["url"] = genre.xpath('@href').get()
            item["name"] = genre.xpath('@data-slug').get()
            yield item

            if item['url'] is not '/':
                next_url = self.start_urls[0] + \
                    item['url'][1:] + 'artistas.html'
                req = Request(next_url, callback=self.artists)
                req.meta['item'] = item
                yield req
