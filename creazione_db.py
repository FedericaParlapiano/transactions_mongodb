from pymongo import MongoClient

client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

db = client['negozio_abbigliamento']
collezione = db['capi_abbigliamento']

documenti = [
    {"_id": 1, "nome": "Maglietta", "prezzo": 19.99, "colore": "rosso", "taglia": "M", "quantità": 50},
    {"_id": 2, "nome": "Jeans", "prezzo": 49.99, "colore": "blu", "taglia": "L", "quantità": 30},
    {"_id": 3, "nome": "Felpa", "prezzo": 39.99, "colore": "grigio", "taglia": "XL", "quantità": 20},
    {"_id": 4, "nome": "Giacca", "prezzo": 89.99, "colore": "nero", "taglia": "M", "quantità": 15},
    {"_id": 5, "nome": "Gonna", "prezzo": 29.99, "colore": "verde", "taglia": "S", "quantità": 40},
    {"_id": 6, "nome": "Pantaloni corti", "prezzo": 24.99, "colore": "beige", "taglia": "M", "quantità": 60},
    {"_id": 7, "nome": "Camicia", "prezzo": 34.99, "colore": "bianco", "taglia": "L", "quantità": 25},
    {"_id": 8, "nome": "Abito", "prezzo": 99.99, "colore": "rosso", "taglia": "S", "quantità": 10},
    {"_id": 9, "nome": "Cappotto", "prezzo": 129.99, "colore": "marrone", "taglia": "XL", "quantità": 5},
    {"_id": 10, "nome": "Maglione", "prezzo": 59.99, "colore": "blu", "taglia": "M", "quantità": 35}
]

# Inserimento dei documenti nella collezione
collezione.insert_many(documenti)

print("Documenti inseriti con successo")