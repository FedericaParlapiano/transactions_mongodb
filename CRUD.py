import pprint

from bson import ObjectId
from pymongo import MongoClient

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)

# get reference to database
db = client.sample_analytics

# get reference to collection
accounts_collection = db.accounts
customers_collection = db.customers
transactions_collection = db.transactions

# INSERT DOCUMENT
new_account = {
    "account_id": 123456,
    "limit": 10000,
    "product": ["Brokerage", "Derivatives", "CurrencyService", "InvestmentFund", "InvestmentStock"]
}

# inserts new_account document into the accounts collection
result = accounts_collection.insert_one(new_account)

document_id = result.inserted_id
print(f"_id of inserted document: {document_id}")

document_to_find = {"_id": ObjectId(document_id)}
pprint.pprint(accounts_collection.find_one(document_to_find))

# FIND DOCUMENT
document_to_find = {"accounts": {"$in": [987709]}}

cursor = customers_collection.find(document_to_find)

num_docs = 0
for document in cursor:
    num_docs += 1
    pprint.pprint(document)
    print()
print("Number of documents found: " + str(num_docs))

# UPDATE DOCUMENT
document_to_update = {"_id": ObjectId(document_id)}
pprint.pprint(accounts_collection.find_one(document_to_update))

add_product = {"$push": {"product": "Inv"}}
result = accounts_collection.update_one(document_to_update, add_product)
print("Documents updated: " + str(result.modified_count))

pprint.pprint(accounts_collection.find_one(document_to_update))

# DELETE DOCUMENT
documents_to_delete = {"account_id": 123456}

result = accounts_collection.delete_many(documents_to_delete)
print("Documents deleted: " + str(result.deleted_count))


client.close()


