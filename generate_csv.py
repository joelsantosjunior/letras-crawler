from pymongo import MongoClient
import re
import csv

client = MongoClient('mongodb://localhost:27017/')

db = client['letras_dataset']
todas_as_musicas = db.musicas.find({})

def hasYear(string):
    if (re.match(r'.*([1-2][0-9]{3})', string) is not None):
        return re.match(r'.*([1-2][0-9]{3})', string).group(1)
    else:
        return ""

def strip(letra):
    return ''.join([ line.strip() + " # " if line is not " " else '' for line in letra ])   

def main ():
    with open('Musicas.csv', mode='w', encoding='utf-8') as csv_file:
        fieldnames = ['genero', 'artista', 'album', 'ano', 'titulo', 'letra', 'compositor']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        for musica in todas_as_musicas:
            try:
                compositor = musica["compositor"][0]
            except:
                compositor = "none"
            row = {
                "genero": musica["genero"]["nome"],
                "artista": musica["artista"],
                "album": musica["album"],
                "ano": hasYear(musica["ano"]),
                "titulo": musica["titulo"],
                "letra": strip(musica["letra"]),
                "compositor": compositor
            }
            writer.writerow(row)

if __name__ == "__main__":
    main()
    