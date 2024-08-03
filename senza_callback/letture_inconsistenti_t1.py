from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client1 = MongoClient(connection_string)

session1 = client1.start_session()
session1.start_transaction(
    read_concern=ReadConcern(level="local"),
    write_concern=WriteConcern(w=1, j=False),
)


db = client1['negozio_abbigliamento']
capiCollection = db['capi_abbigliamento']
capo_id = 1

for i in range(0,3):
    doc = capiCollection.find_one({'capoId': capo_id}, {'_id': False}, session=session1);
    print(doc)
    initial_price = doc.get("prezzo");
    print("Prezzo del capo: ", initial_price);
    print("")
    time.sleep(3)

try:
    session1.commit_transaction()
except Exception as e:
    print(f"\nErrore durante il commit della transazione: {e.args[0]}")
    session1.abort_transaction()

session1.end_session()
client1.close()