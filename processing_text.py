from pymongo import MongoClient
import re

client = MongoClient('mongodb://localhost:27017/')

db = client['letras_dataset']
forro_albums = db.albums.find({"artista.genero.nome": "forro"})
samba_albums = db.albums.find({"artista.genero.nome": "samba"})

def hasYear(string):
    has = re.match(r'.*([1-2][0-9]{3})', string)
    return has is not None

def main ():
    for album in forro_albums:
        if (hasYear(album["info"])):
            musicas = db.musicas.find({"album_id": album["_id"]})
            album["musicas"] = [{
                "nome": item["titulo"],
                "letra": ''.join(item["letra"])
            } for item in musicas]
            print(album)

if __name__ == "__main__":
    main()
    