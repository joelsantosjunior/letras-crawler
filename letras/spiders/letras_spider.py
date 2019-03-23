from scrapy import FormRequest, Request, Spider
from letras.items import Genero, Artista, Album, Musica


class LetrasSpider(Spider):
    name = "letras"
    start_urls = [
        'https://www.letras.mus.br/',
    ]

    def get_musica(self, response):
        '''
        Descrição: Coleta o Titulo, artista, letra e informações do compositor (quando presente)
        '''
        song = {
            "titulo": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h1//text()").get(),
            "artista": response.meta["item"],
            "letra": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[2]/div[1]/p//text()").getall(),
            "compositor": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[4]/div[1]/text()").getall(),
        }
        yield Musica(song)

    def lista_de_musicas(self, response):
        '''
        Descrição: Coleta todas as músicas de um determinado artista
        '''
        musicas = response.css("div.cnt-list--alp")
        for musica in musicas.css("ul.cnt-list > li"):
            link = musica.css("a::attr(href)").get()
            req = Request(self.start_urls[0] + link, callback=self.get_musica)
            req.meta["item"] = response.meta["item"]
            yield req

    def discografia(self, response):
        '''
        Descrição: Usada para coletar todos os albums de um artista
        Dados buscados: Nome, link, info, artista e todas as músicas de cada album
        '''
        albums = response.css('div.cnt-discografia_cd')
        for album in albums:
            info = album.css("div.cnt-discografia_info")
            album_item = {
                "nome": info.css("h4 > a::text").get(),
                "link": info.css("h4 > a::attr(href)").get(),
                "info": info.css("span::text").get(),
                "artista": response.meta["item"],
                "musicas": [{
                    "link": _.css("a::attr(href)").get(),
                    "titulo": _.css("a::attr(title)").get()
                } for _ in album.css("ol.cnt-list > li")]
            }
            yield Album(album_item)

    def todos_os_artistas(self, response):
        '''
        Descrição: Busca todos os artistas de um gênero
        Dados buscados: Gênero, nome e link
        '''
        artists = response.xpath("//ul/li")
        for artista in artists.css("a"):
            item = {
                "genero": response.meta["item"],
                "nome": artista.css("a::text").get(),
                "link": artista.xpath("@href").get()
            }
            yield Artista(item)

            if self.metodo == "discografia":
                next_url = self.start_urls[0] + item["link"][1:] + "discografia"
                req = Request(next_url, callback=self.discografia)
            else:
                next_url = self.start_urls[0] + item["link"][1:]
                req = Request(next_url, callback=self.lista_de_musicas)

            req.meta["item"] = item
            yield req

    def parse(self, response):
        all_genres = response.css('.js-tab-link')

        for genre in all_genres:
            item = Genero()
            item["link"] = genre.xpath('@href').get()
            item["nome"] = genre.xpath('@data-slug').get()
            if item["link"] != "/estilos//" and item["nome"] == self.genero:
                # yield item
                next_url = self.start_urls[0] + item['link'][1:] + 'todosartistas.html'
                req = Request(next_url, callback=self.todos_os_artistas)
                req.meta['item'] = item
                yield req
