from datetime import datetime
from bson import Decimal128
from pymongo import MongoClient

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

db = client['negozio_abbigliamento']
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
        "nome": "Abito", "prezzo": Decimal128("99.99"), "colore": "beige",
        "disponibilita": {"S": 15, "M": 10, "L": 5}
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

collezione.insert_many(documents=documenti)

print("Documenti inseriti con successo")


collezione_scontrini = db['scontrini']
collezione_scontrini.delete_many({})

scontrini = [
    {
        "data": datetime.strptime("2024-07-01", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglietta", "quantita": 2, "prezzo_totale":
                Decimal128("39.98"), "taglia": "M"},
            {"nome": "Jeans", "quantita": 1, "prezzo_totale":
                Decimal128("49.99"), "taglia": "XS"}
        ],
        "totale_complessivo": Decimal128("89.97")
    },
    {
        "data": datetime.strptime("2024-07-02", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": 1, "prezzo_totale":
                Decimal128("39.99"), "taglia": "L"},
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale":
                Decimal128("129.99"), "taglia": "XS"}
        ],
        "totale_complessivo": Decimal128("169.98")
    },
    {
        "data": datetime.strptime("2024-07-03", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Gonna", "quantita": 3, "prezzo_totale":
                Decimal128("89.97"), "taglia": "XS"},
            {"nome": "Maglietta", "quantita": 1, "prezzo_totale":
                Decimal128("19.99"), "taglia": "XL"}
        ],
        "totale_complessivo": Decimal128("109.96")
    },
    {
        "data": datetime.strptime("2024-07-04", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Camicia", "quantita": 2, "prezzo_totale":
                Decimal128("69.98"), "taglia": "XS"},
            {"nome": "Pantaloni corti", "quantita": 1, "prezzo_totale":
                Decimal128("24.99"), "taglia": "M"}
        ],
        "totale_complessivo": Decimal128("94.97")
    },
    {
        "data": datetime.strptime("2024-07-05", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita": 1, "prezzo_totale":
                Decimal128("99.99"), "taglia": "M"},
            {"nome": "Maglione", "quantita": 1, "prezzo_totale":
                Decimal128("59.99"), "taglia": "M"}
        ],
        "totale_complessivo": Decimal128("159.98")
    },
    {
        "data": datetime.strptime("2024-07-06", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Giacca", "quantita": 1, "prezzo_totale":
                Decimal128("89.99"), "taglia": "S"},
            {"nome": "Jeans", "quantita": 1, "prezzo_totale":
                Decimal128("49.99"), "taglia": "XS"}
        ],
        "totale_complessivo": Decimal128("139.98")
    },
    {
        "data": datetime.strptime("2024-07-07", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": 2, "prezzo_totale":
                Decimal128("79.98"), "taglia": "XS"},
            {"nome": "Maglietta", "quantita": 3, "prezzo_totale":
                Decimal128("59.97"), "taglia": "XS"}
        ],
        "totale_complessivo": Decimal128("139.95")
    },
    {
        "data": datetime.strptime("2024-07-08", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale":
                Decimal128("129.99"), "taglia": "XL"},
            {"nome": "Gonna", "quantita": 2, "prezzo_totale":
                Decimal128("59.98"), "taglia": "XL"}
        ],
        "totale_complessivo": Decimal128("189.97")
    },
    {
        "data": datetime.strptime("2024-07-09", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Abito", "quantita": 2, "prezzo_totale":
                Decimal128("199.98"), "taglia": "XS"},
            {"nome": "Camicia", "quantita": 1, "prezzo_totale":
                Decimal128("34.99"), "taglia": "M"}
        ],
        "totale_complessivo": Decimal128("234.97")
    },
    {
        "data": datetime.strptime("2024-07-10", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Maglione", "quantita": 1, "prezzo_totale":
                Decimal128("59.99"), "taglia": "XS"},
            {"nome": "Pantaloni corti", "quantita": 2, "prezzo_totale":
                Decimal128("49.98"), "taglia": "XL"}
        ],
        "totale_complessivo": Decimal128("109.97")
    }
]

collezione_scontrini.insert_many(documents=scontrini)


print("Scontrini inseriti con successo")

'''
db.capi_abbigliamento.insert_one({
    "nome": "Maglietta",
    "prezzo": Decimal128("19.99"),
    "colore": "rosso",
    "disponibilita": {"S": 30, "M": 50, "L": 20, "K":2}
})
'''
'''
db.capi_abbigliamento.insert_one({
        "prezzo": Decimal128("19.99"),
        "colore": "rosso",
        "disponibilita": {"S": 30, "M": 50, "L": 20, "XL": 2}
})
'''
'''
db.scontrini.insert_one({
        "data": datetime.strptime("2024-07-10", "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": -1, "prezzo_totale": Decimal128("39.99"), "taglia":"XL"},
            {"nome": "Cappotto", "quantita": 1, "prezzo_totale": Decimal128("129.99"), "taglia":"XL"}
        ],
        "totale_complessivo": Decimal128("69.98")
})
'''