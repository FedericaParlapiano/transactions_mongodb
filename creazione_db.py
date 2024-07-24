from datetime import datetime

from pymongo import MongoClient

client = MongoClient('mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10')

db = client['negozio_abbigliamento']
collezione = db['capi_abbigliamento']

collezione.drop()

documenti = [
    {"_id": 1, "nome": "Maglietta", "prezzo": 19.99, "colore": "rosso", "taglia": "M", "quantita'": 50},
    {"_id": 2, "nome": "Jeans", "prezzo": 49.99, "colore": "blu", "taglia": "L", "quantita'": 30},
    {"_id": 3, "nome": "Felpa", "prezzo": 39.99, "colore": "grigio", "taglia": "XL", "quantita'": 20},
    {"_id": 4, "nome": "Giacca", "prezzo": 89.99, "colore": "nero", "taglia": "M", "quantita'": 15},
    {"_id": 5, "nome": "Gonna", "prezzo": 29.99, "colore": "verde", "taglia": "S", "quantita'": 40},
    {"_id": 6, "nome": "Pantaloni corti", "prezzo": 49.99, "colore": "beige", "taglia": "M", "quantita'": 60},
    {"_id": 7, "nome": "Camicia", "prezzo": 34.99, "colore": "bianco", "taglia": "L", "quantita'": 25},
    {"_id": 8, "nome": "Abito", "prezzo": 99.99, "colore": "rosso", "taglia": "S", "quantita'": 10},
    {"_id": 9, "nome": "Cappotto", "prezzo": 129.99, "colore": "marrone", "taglia": "XL", "quantita'": 5},
    {"_id": 10, "nome": "Maglione", "prezzo": 59.99, "colore": "blu", "taglia": "M", "quantita'": 35}
]

collezione.insert_many(documenti)

print("Documenti inseriti con successo")


db = client['negozio_abbigliamento']
collezione_scontrini = db['scontrini']

collezione_scontrini.drop()

scontrini = [
    {
        "_id": 1,
        "data": datetime.strptime("2024-07-01", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglietta", "quantita'": 2, "prezzo_totale": 39.98},
            {"nome": "Jeans", "quantita'": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 89.97
    },
    {
        "_id": 2,
        "data": datetime.strptime("2024-07-02", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita'": 1, "prezzo_totale": 39.99},
            {"nome": "Cappotto", "quantita'": 1, "prezzo_totale": 129.99}
        ],
        "totale_complessivo": 169.98
    },
    {
        "_id": 3,
        "data": datetime.strptime("2024-07-03", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Gonna", "quantita'": 3, "prezzo_totale": 89.97},
            {"nome": "Maglietta", "quantita'": 1, "prezzo_totale": 19.99}
        ],
        "totale_complessivo": 109.96
    },
    {
        "_id": 4,
        "data": datetime.strptime("2024-07-04", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Camicia", "quantita'": 2, "prezzo_totale": 69.98},
            {"nome": "Pantaloni corti", "quantita'": 1, "prezzo_totale": 24.99}
        ],
        "totale_complessivo": 94.97
    },
    {
        "_id": 5,
        "data": datetime.strptime("2024-07-05", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita'": 1, "prezzo_totale": 99.99},
            {"nome": "Maglione", "quantita'": 1, "prezzo_totale": 59.99}
        ],
        "totale_complessivo": 159.98
    },
    {
        "_id": 6,
        "data": datetime.strptime("2024-07-06", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Giacca", "quantita'": 1, "prezzo_totale": 89.99},
            {"nome": "Jeans", "quantita'": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 139.98
    },
    {
        "_id": 7,
        "data": datetime.strptime("2024-07-07", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita'": 2, "prezzo_totale": 79.98},
            {"nome": "Maglietta", "quantita'": 3, "prezzo_totale": 59.97}
        ],
        "totale_complessivo": 139.95
    },
    {
        "_id": 8,
        "data": datetime.strptime("2024-07-08", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantita'": 1, "prezzo_totale": 129.99},
            {"nome": "Gonna", "quantita'": 2, "prezzo_totale": 59.98}
        ],
        "totale_complessivo": 189.97
    },
    {
        "_id": 9,
        "data": datetime.strptime("2024-07-09", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita'": 2, "prezzo_totale": 199.98},
            {"nome": "Camicia", "quantita'": 1, "prezzo_totale": 34.99}
        ],
        "totale_complessivo": 234.97
    },
    {
        "_id": 10,
        "data": datetime.strptime("2024-07-10", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglione", "quantita'": 1, "prezzo_totale": 59.99},
            {"nome": "Pantaloni corti", "quantita'": 2, "prezzo_totale": 49.98}
        ],
        "totale_complessivo": 109.97
    }
]

collezione_scontrini.insert_many(scontrini)

print("Scontrini inseriti con successo")
