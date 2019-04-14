from scrapy import FormRequest, Request, Spider
from letras.items import Musica
import re


class LetrasSpider(Spider):
    name = "letras"
    start_urls = [
        'https://www.letras.mus.br/',
    ]

    def getYear(self, text):
        return re.match(r'.*([1-2][0-9]{3})', text).group(1)

    def parse(self, response):
        all_genres = response.css('.js-tab-link')

        for genre in all_genres:
            item = {}
            item["link"] = genre.xpath('@href').get()
            item["nome"] = genre.xpath('@data-slug').get()
            if item["link"] != "/estilos//" and item["nome"] == self.genero:
                # yield item
                next_url = self.start_urls[0] + item['link'][1:] + 'todosartistas.html'
                req = Request(next_url, callback=self.todos_os_artistas)
                req.meta['item'] = item
                yield req
    
    def todos_os_artistas(self, response):
        '''
        Descrição: Busca todos os artistas de um gênero
        Dados buscados: Gênero, nome e link
        '''
        artists = response.xpath("//ul/li")
        for artista in artists.css("a"):
            item = {
                "genero": response.meta["item"],
                "artista": artista.css("a::text").get(),
                "link": artista.xpath("@href").get()
            }

            if self.metodo == "discografia":
                next_url = self.start_urls[0] + item["link"][1:] + "discografia"
                req = Request(next_url, callback=self.discografia)
                req.meta["item"] = item
                yield req
            else:
                next_url = self.start_urls[0] + item["link"][1:]
                req = Request(next_url, callback=self.lista_de_musicas)
                req.meta["item"] = item
                yield req


    def discografia(self, response):
        '''
        Descrição: Usada para coletar todos os albums de um artista
        Dados buscados: Nome, link, info, artista e todas as músicas de cada album
        '''
        albums = response.css('div.cnt-discografia_cd')
        for album in albums:
            info = album.css("div.cnt-discografia_info")
            musicas = [{"link": _.css("a::attr(href)").get(),
                        "titulo": _.css("a::attr(title)").get()} 
                        for _ in album.css("ol.cnt-list > li")]
            for musica in musicas:
                next_url = self.start_urls[0] + musica["link"][1:]
                req = Request(next_url, callback=self.get_musica)
                req.meta["item"] = {
                    "genero": response.meta["item"]["genero"],
                    "artista": response.meta["item"]["artista"],
                    "album": info.css("h4 > a::text").get(),
                    "info": info.css("span::text").get(),
                    "link": next_url
                }
                yield req
            

    def lista_de_musicas(self, response):
        '''
        Descrição: Coleta todas as músicas de um determinado artista
        '''
        musicas = response.css("div.cnt-list--alp")
        for musica in musicas.css("ul.cnt-list > li"):
            link = musica.css("a::attr(href)").get()
            req = Request(self.start_urls[0] + link, callback=self.get_musica)
            response.meta["item"]["link"] = link
            req.meta["item"] = response.meta["item"]
            yield req

    def get_musica(self, response):
        '''
        Descrição: Coleta o Titulo, artista, letra e informações do compositor (quando presente)
        '''
        song = {
            "genero": response.meta["item"]["genero"],
            "artista": response.meta["item"]["artista"],
            "album": response.meta["item"]["album"],
            "ano": response.meta["item"]["info"],
            "link": response.meta["item"]["link"],
            "titulo": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[1]/div[2]/h1//text()").get(),
            "letra": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[2]/div[1]/p//text()").getall(),
            "compositor": response.xpath("//*[@id=\"js-lyric-cnt\"]/article/div[4]/div[1]/text()").getall(),
        }
        yield Musica(song)

    

    
