from bson import Decimal128
from pymongo import MongoClient, WriteConcern
from pymongo.errors import PyMongoError
from pymongo.read_concern import ReadConcern
import time

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"
client = MongoClient(connection_string)

def callback(session):
    capiCollection = session.client.negozio_abbigliamento.capi_abbigliamento.with_options(
        write_concern=WriteConcern(w=1, j=False)
    )

    try:

        abito = capiCollection.find_one({'nome': 'Abito'}, session=session)
        prezzo_abito = abito.get("prezzo").to_decimal()

        giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session)
        prezzo_giacca = giacca.get("prezzo").to_decimal()
        pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session)
        prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

        prezzo_completo = prezzo_giacca + prezzo_pantaloni

        print("T2 - Prezzo giacca prima dell'update: ", prezzo_giacca)
        print("T2 - Prezzo pantaloni prima dell'update: ", prezzo_pantaloni)
        print("T2 - Prezzo completo giacca e pantaloni: ", round(float(prezzo_completo), 2))
        print("T2 - Prezzo cappotto: ", prezzo_abito)
        print("")

        # Verifica della condizione e aggiornamento del prezzo
        if prezzo_completo >= prezzo_abito + 20:

            time.sleep(4)
            capiCollection.update_one({'nome': 'Pantaloni'}, {'$set': {'prezzo': Decimal128(prezzo_pantaloni-40)}}, session=session)

            pantaloni = capiCollection.find_one({'nome': 'Pantaloni'}, session=session)
            prezzo_pantaloni = pantaloni.get("prezzo").to_decimal()

            print("T2 - Prezzo pantaloni dopo l'update: ", prezzo_pantaloni)
            print("")

            capiCollection.update_one({'nome': 'Giacca'}, {'$set': {'prezzo': Decimal128(prezzo_giacca+40)}},
                                    session=session)

            giacca = capiCollection.find_one({'nome': 'Giacca'}, session=session)
            prezzo_giacca = giacca.get("prezzo").to_decimal()
            print("T2 - Prezzo giacca dopo l'update: ", prezzo_giacca)
            print("")

            session.commit_transaction()
            print("T2 - Commit")
            print("")
        else:
            session.abort_transaction()
            print("T2 - Abort: il prezzo del completo deve superare quello dell'cappotto")
            print("")
    finally:
        session.end_session()

def callback_wrapper(s):
    callback(
        session=s
    )


with client.start_session() as session:
    try:
        session.with_transaction(
            callback_wrapper,
            read_concern=ReadConcern(level="local"),
            write_concern=WriteConcern(w=1, j=False)
        )
    except PyMongoError as e:
        print(f"Transazione fallita: {e.args[0]}")

client.close()
