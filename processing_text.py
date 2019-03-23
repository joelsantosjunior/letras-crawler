from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')

db = client['letras_dataset']

sambas = db.sambaenredo.find()

for samba in sambas:
    letra = [linha.strip() for linha in samba['letra']]
    letra = ''.join(samba['letra'])
    print(letra)

