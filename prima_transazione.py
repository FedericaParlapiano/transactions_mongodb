from datetime import datetime
from pymongo import MongoClient

connection_string = "..."
client = MongoClient(connection_string)

def callback(session, articolo=None, taglia=None):

    capi_abbigliamento = session.client.negozio_abbigliamento.capi_abbigliamento
    scontrini = session.client.negozio_abbigliamento.scontrini

    articolo = capi_abbigliamento.find_one({'nome': articolo}, session=session)
    prezzo_articolo = articolo.get("prezzo")

    campo_da_aggiornare = f"disponibilita.{taglia}"

    capi_abbigliamento.update_one(
        {"nome": "Felpa"},
        {"$inc": {campo_da_aggiornare: -1}},
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
        "L"
    )

with client.start_session() as session:
    session.with_transaction(callback_wrapper)


client.close()
