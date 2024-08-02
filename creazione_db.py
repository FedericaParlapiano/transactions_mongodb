from datetime import datetime
from bson import Decimal128, ObjectId
from pymongo import MongoClient

client = MongoClient("mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client['negozio_abbigliamento']

counters = db['counters']
counters.delete_many({})

collezione = db['capi_abbigliamento']
collezione.delete_many({})

documenti = [
    {
        "nome": "Maglietta",
        "prezzo": Decimal128("19.99"),
        "colore": "rosso",
        "disponibilita": {"S": 30, "M": 50, "L": 20}
    },
    {
        "nome": "Jeans",
        "prezzo": Decimal128("49.99"),
        "colore": "blu",
        "disponibilita": {"S": 25, "M": 60, "L": 40, "XL": 15}
    },
    {
        "nome": "Felpa",
        "prezzo": Decimal128("39.99"),
        "colore": "grigio",
        "disponibilita": {"M": 25, "L": 15, "XL": 30}
    },
    {
        "nome": "Giacca",
        "prezzo": Decimal128("74.99"),
        "colore": "beige",
        "disponibilita": {"S": 10, "M": 15, "L": 8}
    },
    {
        "nome": "Gonna",
        "prezzo": Decimal128("29.99"),
        "colore": "verde",
        "disponibilita": {"S": 40, "M": 30}
    },
    {
        "nome": "Pantaloni corti",
        "prezzo": Decimal128("24.99"),
        "colore": "blu",
        "disponibilita": {"S": 20, "M": 60, "L": 30}
    },
    {
        "nome": "Pantaloni",
        "prezzo": Decimal128("49.99"),
        "colore": "beige",
        "disponibilita": {"S": 10, "M": 60, "L": 20}
    },
    {
        "nome": "Camicia",
        "prezzo": Decimal128("34.99"),
        "colore": "bianco",
        "disponibilita": {"S": 20, "M": 15, "L": 25, "XL": 10}
    },
    {
        "nome": "Abito", "prezzo": Decimal128("99.99"), "colore": "beige", "disponibilita": {"S": 15, "M": 10, "L": 5}
    },
    {
        "nome": "Cappotto",
        "prezzo": Decimal128("129.99"),
        "colore": "marrone",
        "disponibilita": {"M": 8, "L": 5, "XL": 10}
    },
    {
        "nome": "Maglione",
        "prezzo": Decimal128("59.99"),
        "colore": "blu",
        "disponibilita": {"S": 10, "M": 35, "L": 20, "XL": 15}
    }
]

for doc in documenti:
    collezione.insert_one(doc)

print("Documenti inseriti con successo")


db = client['negozio_abbigliamento']
collezione_scontrini = db['scontrini']

collezione_scontrini.delete_many({})

scontrini = [
    {
        "data": datetime.strptime("2024-07-01", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglietta", "quantita": 2, "prezzo_totale": 39.98},
            {"nome": "Jeans", "quantita": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 89.97
    },
    {
        "data": datetime.strptime("2024-07-02", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": 1, "prezzo_totale": 39.99},
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale": 129.99}
        ],
        "totale_complessivo": 169.98
    },
    {
        "data": datetime.strptime("2024-07-03", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Gonna", "quantita": 3, "prezzo_totale": 89.97},
            {"nome": "Maglietta", "quantita": 1, "prezzo_totale": 19.99}
        ],
        "totale_complessivo": 109.96
    },
    {
        "data": datetime.strptime("2024-07-04", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Camicia", "quantita": 2, "prezzo_totale": 69.98},
            {"nome": "Pantaloni corti", "quantita": 1, "prezzo_totale": 24.99}
        ],
        "totale_complessivo": 94.97
    },
    {
        "data": datetime.strptime("2024-07-05", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita": 1, "prezzo_totale": 99.99},
            {"nome": "Maglione", "quantita": 1, "prezzo_totale": 59.99}
        ],
        "totale_complessivo": 159.98
    },
    {
        "data": datetime.strptime("2024-07-06", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Giacca", "quantita": 1, "prezzo_totale": 89.99},
            {"nome": "Jeans", "quantita": 1, "prezzo_totale": 49.99}
        ],
        "totale_complessivo": 139.98
    },
    {
        "data": datetime.strptime("2024-07-07", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": 2, "prezzo_totale": 79.98},
            {"nome": "Maglietta", "quantita": 3, "prezzo_totale": 59.97}
        ],
        "totale_complessivo": 139.95
    },
    {
        "data": datetime.strptime("2024-07-08", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale": 129.99},
            {"nome": "Gonna", "quantita": 2, "prezzo_totale": 59.98}
        ],
        "totale_complessivo": 189.97
    },
    {
        "data": datetime.strptime("2024-07-09", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita": 2, "prezzo_totale": 199.98},
            {"nome": "Camicia", "quantita": 1, "prezzo_totale": 34.99}
        ],
        "totale_complessivo": 234.97
    },
    {
        "data": datetime.strptime("2024-07-10", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglione", "quantita": 1, "prezzo_totale": 59.99},
            {"nome": "Pantaloni corti", "quantita": 2, "prezzo_totale": 49.98}
        ],
        "totale_complessivo": 109.97
    }
]

for doc in scontrini:
    collezione_scontrini.insert_one(doc)

print("Scontrini inseriti con successo")