from datetime import datetime

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

collezione.insert_many(documenti)

print("Documenti inseriti con successo")


db = client['negozio_abbigliamento']
collezione_scontrini = db['scontrini']

scontrini = [
    {
        "_id": 1,
        "data": datetime.strptime("2024-07-01", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglietta", "quantità": 2, "prezzo_totale": 39.98},
            {"nome": "Jeans", "quantità": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 89.97
    },
    {
        "_id": 2,
        "data": datetime.strptime("2024-07-02", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantità": 1, "prezzo_totale": 39.99},
            {"nome": "Cappotto", "quantità": 1, "prezzo_totale": 129.99}
        ],
        "totale_complessivo": 169.98
    },
    {
        "_id": 3,
        "data": datetime.strptime("2024-07-03", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Gonna", "quantità": 3, "prezzo_totale": 89.97},
            {"nome": "Maglietta", "quantità": 1, "prezzo_totale": 19.99}
        ],
        "totale_complessivo": 109.96
    },
    {
        "_id": 4,
        "data": datetime.strptime("2024-07-04", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Camicia", "quantità": 2, "prezzo_totale": 69.98},
            {"nome": "Pantaloni corti", "quantità": 1, "prezzo_totale": 24.99}
        ],
        "totale_complessivo": 94.97
    },
    {
        "_id": 5,
        "data": datetime.strptime("2024-07-05", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantità": 1, "prezzo_totale": 99.99},
            {"nome": "Maglione", "quantità": 1, "prezzo_totale": 59.99}
        ],
        "totale_complessivo": 159.98
    },
    {
        "_id": 6,
        "data": datetime.strptime("2024-07-06", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Giacca", "quantità": 1, "prezzo_totale": 89.99},
            {"nome": "Jeans", "quantità": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 139.98
    },
    {
        "_id": 7,
        "data": datetime.strptime("2024-07-07", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantità": 2, "prezzo_totale": 79.98},
            {"nome": "Maglietta", "quantità": 3, "prezzo_totale": 59.97}
        ],
        "totale_complessivo": 139.95
    },
    {
        "_id": 8,
        "data": datetime.strptime("2024-07-08", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantità": 1, "prezzo_totale": 129.99},
            {"nome": "Gonna", "quantità": 2, "prezzo_totale": 59.98}
        ],
        "totale_complessivo": 189.97
    },
    {
        "_id": 9,
        "data": datetime.strptime("2024-07-09", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantità": 2, "prezzo_totale": 199.98},
            {"nome": "Camicia", "quantità": 1, "prezzo_totale": 34.99}
        ],
        "totale_complessivo": 234.97
    },
    {
        "_id": 10,
        "data": datetime.strptime("2024-07-10", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglione", "quantità": 1, "prezzo_totale": 59.99},
            {"nome": "Pantaloni corti", "quantità": 2, "prezzo_totale": 49.98}
        ],
        "totale_complessivo": 109.97
    }
]

# Inserimento dei documenti nella collezione
collezione_scontrini.insert_many(scontrini)

print("Scontrini inseriti con successo")
