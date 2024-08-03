from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client2 = MongoClient(connection_string)


def callback(session, capo_id=None):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        read_concern=ReadConcern("local"),
        write_concern=WriteConcern(w=1, j=False)
    )

    doc = capiCollection.find_one(
        {'capoId': capo_id},
        {'_id': False},
        session=session,
    )
    print(doc)
    initial_price = doc.get("prezzo").to_decimal()
    print("Prezzo del capo: ", initial_price)

    try:
        session.commit_transaction()
        print("\n\nTransazione andata a buon fine.\n")
    except Exception as e:
        print(f"\n\nErrore durante il commit della transazione: {e.args[0]}")
        session.abort_transaction()
        return



def callback_wrapper(s):
    callback(
        session=s,
        capo_id=1,
    )


with client2.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client2.close()