import pprint

from bson import ObjectId, Decimal128
from pymongo import MongoClient

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

db = client.negozio_abbigliamento

capi_abbigliamento = db.capi_abbigliamento
scontrini = db.scontrini

nuovo_capo = {
        "nome": "Collana",
        "prezzo": Decimal128("29.99"),
        "colore": "oro",
        "disponibilita": {"S": 2, "M": 5, "L": 2}
    }

result = capi_abbigliamento.insert_one(nuovo_capo)

document_id = result.inserted_id
print(f"_id del documento inserito: {document_id}")

document_to_find = {"_id": ObjectId(document_id)}
pprint.pprint(capi_abbigliamento.find_one(document_to_find))

document_to_find = {"_id": ObjectId(document_id)}

cursor = capi_abbigliamento.find(document_to_find)

num_docs = 0
for document in cursor:
    num_docs += 1
    pprint.pprint(document)
    print()
print("Numero di documenti trovati: " + str(num_docs))

document_to_update = {"_id": ObjectId(document_id)}
pprint.pprint(capi_abbigliamento.find_one(document_to_update))

add_product = {"$inc": {"prezzo": Decimal128("10")}}
result = capi_abbigliamento.update_one(document_to_update, add_product)
print("Documenti aggiornati: " + str(result.modified_count))

pprint.pprint(capi_abbigliamento.find_one(document_to_update))

documents_to_delete = {"nome": "Collana"}

result = capi_abbigliamento.delete_many(documents_to_delete)
print("Documenti eliminati: " + str(result.deleted_count))


client.close()


