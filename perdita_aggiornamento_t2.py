from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
import time

connection_string = "..."
client2 = MongoClient(connection_string)


def callback(session, capo_id=None, additional_price=0):
    myCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )

    doc = myCollection.find_one(
        {'capoId': capo_id},
        session=session,
    )
    print("Documento da modificare: ", doc)
    initial_price = doc.get("prezzo").to_decimal()
    print("Prezzo iniziale: ", initial_price)

    time.sleep(3)

    try:
        myCollection.update_one({'capoId': capo_id},
                                {"$set": {"prezzo": Decimal128(initial_price + additional_price)}},
                                session=session)

        modified_doc = myCollection.find_one(
            {'capoId': capo_id},
            session=session,
        )
        final_price = modified_doc.get("prezzo").to_decimal()
        print("\n\nDocumento modificato: ", modified_doc)
        print("Prezzo finale: ", final_price)

        try:
            session.commit_transaction()
            print("\n\nTransazione andata a buon fine.\n")
        except Exception as e:
            print(f"\n\nErrore durante il commit della transazione: {e.args[0]}")
            session.abort_transaction()

    except Exception as e:
        print(f"\n\nErrore durante l'aggiornamento: {e.args[0]}")
        print("\n\nTransazione abortita. \n")

    return


def callback_wrapper(s):
    callback(
        session=s,
        capo_id=1,
        additional_price=10
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
