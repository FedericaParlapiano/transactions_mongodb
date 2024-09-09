from pymongo import MongoClient

connection_string = "..."
client = MongoClient(connection_string)

db = client['negozio_abbigliamento']

validator = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Validazione dei documenti della collezione capi_abbigliamento",
        "required": ["prezzo", "nome", "disponibilita"],
        "properties": {
            "nome": {
                "bsonType": "string",
                "description": "nome deve essere una stringa ed e' obbligatorio"
            },
            "prezzo": {
                "bsonType": "decimal",
                "minimum": 0,
                "maximum": 10000,
                "description": "prezzo deve essere un Decimal128 positivo"
            },
            "disponibilita": {
                "bsonType": "object",
                "properties": {
                    "XS": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "XS deve essere un intero maggiore di 0"
                    },
                    "S": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "S deve essere un intero maggiore di 0"
                    },
                    "M": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "M deve essere un intero maggiore di 0"
                    },
                    "L": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "L deve essere un intero maggiore di 0"
                    },
                    "XL": {
                        "bsonType": "int",
                        "minimum": 0,
                        "description": "XL deve essere un intero maggiore di 0"
                    }
                },
                "patternProperties": {
                    "^(?!XS|S|M|L|XL$).*": {
                        "bsonType": "null",
                        "description": "Nessun'altra chiave e' permessa in disponibilita"
                    }
                },
                "description": "disponibilita deve essere un oggetto con chiavi 'XS', 'S', 'M', 'L', 'XL' e con valori interi positivi"
            }
        }
    }
}

db.create_collection(
    'capi_abbigliamento',
    validator=validator
)

print("La collezione capi_abbigliamento è stata correttamente creata con lo schema di validazione.")



validator_scontrini = {
    "$jsonSchema": {
        "bsonType": "object",
        "title": "Validazione dei documenti inseriti nella collection scontrini",
        "required": ["data", "articoli", "totale_complessivo"],
        "properties": {
            "data": {
                "bsonType": "date",
                "description": "data deve essere una data ed e' obbligatorio"
            },
            "articoli": {
                "bsonType": "array",
                "items": {
                    "bsonType": "object",
                    "required": ["nome", "quantita", "taglia", "prezzo_totale"],
                    "properties": {
                        "nome": {
                            "bsonType": "string",
                            "description": "nome deve essere una stringa ed e' obbligatorio"
                        },
                        "quantita": {
                            "bsonType": "int",
                            "minimum": 1,
                            "description": "quantita deve essere un intero maggiore o uguale a 1"
                        },
                        "taglia": {
                            "bsonType": "string",
                            "enum": ["XS", "S", "M", "L", "XL"],
                            "description": "taglia deve essere una delle seguenti: 'XS', 'S', 'M', 'L', 'XL'"
                        },
                        "prezzo_totale": {
                            "bsonType": "decimal",
                            "minimum": 0,
                            "description": "prezzo_totale deve essere un numero positivo"
                        }
                    }
                },
                "description": "articoli deve essere un array di oggetti articoli"
            },
            "totale_complessivo": {
                "bsonType": "decimal",
                "minimum": 0,
                "description": "totale_complessivo deve essere un numero positivo e rappresenta la somma dei prezzi totali degli articoli"
            }
        }
    }
}

db.create_collection(
    'scontrini',
    validator=validator_scontrini
)

print("La collezione scontrini è stata correttamente creata con lo schema di validazione.")


