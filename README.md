<h1 align="center"> Transazioni e anomalie in MongoDB </h1>

Questa repository è relativa alla sperimentazione del comportamento delle transazioni.
La sperimentazione ha dimostrato che MongoDB ha una buona capacità di gestione delle anomalie generalmente considerate in letteratura, che altri DBMS, tra cui MySQL, non sono in grado di evitare in maniera assoluta.

## Requisiti
* MongoDB 7.0 o versioni successive
* PyMongo
* Configurazione di un cluster su MongoDB Atlas

## Dati
Il database utilizzato, _negozio_abbigliamento_, archivia informazioni su articoli di abbigliamento disponibili in un negozio e sugli acquisti effettuati. 
Esso si compone di due collezioni principali:
- collezione _capi_abbigliamento_, che contiene i dati relativi agli articoli di abbigliamento disponibili nel negozio,
- collezione _scontrini_, che registra gli acquisti avvenute, inclusi i dettagli degli articoli acquistati e il totale complessivo.
Per creare il database è sufficiente eseguire il file [creazione_db.py](https://github.com/FedericaParlapiano/transactions_mongodb/blob/master/creazione_db.py) e poi, per inserire dei dati di prova, il file [popolamento_db.py](https://github.com/FedericaParlapiano/transactions_mongodb/blob/master/popolamento_db.py).

## Test
Per valutare il comportamento rispetto alle anomalie sono stati predeisposti coppie di file .py. Ciascuna coppia di file deve essere eseguita in maniera simultanea, su due terminali differenti.

### Autori
Progetto realizzato da:
- [Parlapiano Federica](https://github.com/FedericaParlapiano)
- [Ronci Arianna](https://github.com/AriannaRonci)
