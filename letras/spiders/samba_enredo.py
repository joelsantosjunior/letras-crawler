from scrapy import Spider, Request

class classname(Spider):
    name = "sambaenredo"
    baseurl = "https://www.letras.mus.br/"
    start_urls = ["http://localhost:8000/samba-enredo.html"]

    def parse(self, response):
        lista = response.css("div.home-artistas > .cnt-list .cnt-list--col3")
        print(lista)
