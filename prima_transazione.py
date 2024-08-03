# Connect to MongoDB cluster with MongoClient
from datetime import datetime

from bson import Decimal128
from pymongo import MongoClient

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

# Step 1: Define the callback that specifies the sequence of operations to perform inside the transactions.
def callback(session, account_id=None, new_account_id=None):

    capi_abbigliamento = session.client.negozio_abbigliamento.capi_abbigliamento
    scontrini = session.client.negozio_abbigliamento.scontrini

    articolo = capi_abbigliamento.find_one({'nome': "Felpa"}, session=session)
    prezzo_articolo = articolo.get("prezzo")

    capi_abbigliamento.update_one(
        {"nome": "Felpa"},
        {"$inc": {"disponibilita.L": -1}},
        session=session,
    )

    scontrino_da_inserire = {
        "data": datetime.strptime(str(datetime.now().date()), "%Y-%m-%d"),
        "articoli": [
            {"nome": "Felpa", "quantita": 1, "prezzo_totale": prezzo_articolo, "taglia": "L"},
        ],
        "totale_complessivo": prezzo_articolo
    }

    scontrini.insert_one(
        scontrino_da_inserire,
        session=session,
    )

    print("Transaction successful")

    return


def callback_wrapper(s):
    callback(
        s,
        "Felpa",
        121212
    )


# Step 2: Start a client session
with client.start_session() as session:
    # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or cancel on error)
    session.with_transaction(callback_wrapper)


client.close()