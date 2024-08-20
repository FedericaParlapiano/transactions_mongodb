from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference

import time

connection_string = "..."

client1 = MongoClient(connection_string)


def callback(session, capo_id=None, additional_price=0):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        read_concern=ReadConcern("local"),
        write_concern=WriteConcern(w=1, j=False)
    )

    doc = capiCollection.find_one(
        {'capoId': capo_id},
        {'_id': False},
        session=session,
    )
    print("Documento da modificare: ", doc)
    initial_price = doc.get("prezzo").to_decimal()
    print("Prezzo iniziale: ", initial_price)

    try:
        capiCollection.update_one({'capoId': capo_id},
                                  {"$set": {"prezzo": Decimal128(initial_price + additional_price)}},
                                  session=session)

        modified_doc = capiCollection.find_one(
            {'capoId': capo_id},
            {'_id': False},
            session=session,
        )
        final_price = modified_doc.get("prezzo").to_decimal()
        print("\nDocumento modificato: ", modified_doc)
        print("Prezzo finale: ", final_price)

        time.sleep(2)

        try:
            session.commit_transaction()
            print("\n\nTransazione andata a buon fine.\n")
        except Exception as e:
            print(f"\n\nErrore durante il commit della transazione: {e.args[0]}")
            session.abort_transaction()
            return

    except Exception as e:
        print(f"\n\nErrore durante l'aggiornamento: {e.args[0]}")
        print("\nTransazione abortita. \n")
        session.abort_transaction()
        return


def callback_wrapper(s):
    callback(
        session=s,
        capo_id=1,
        additional_price=5
    )


with client1.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client1.close()
