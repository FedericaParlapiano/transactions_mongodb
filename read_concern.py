from pymongo import MongoClient
from pymongo.read_concern import ReadConcern
from pymongo import WriteConcern

connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"


def make_payment(url, payment, account_type, do_conflict_check):
    client = MongoClient(url, readConcernLevel='majority', readPreference='primary')
    acc_coll = client[DB_NAME][ACC_COLL_NAME]

    try:
        with client.start_session() as tx_sess:
            with tx_sess.start_transaction(read_concern=ReadConcern(level='snapshot'),
                                           write_concern=WriteConcern('majority')):
                # READ BALANCES FOR ALICE'S CURRENT & SAVING ACCOUNTS AND TOTAL THEM UP
                aliceBalance = getAliceCurrentBalance(tx_sess, acc_coll, do_conflict_check)

                # STOP PROCESSING THE PAYMENT ALICE DOES NOT HAVE ENOUGH FUNDS
                if (aliceBalance - Decimal(payment)) < 0:
                    print(f" - Correctly refusing payment of '{payment}' because Alice's bank "
                          f"balance is: '{aliceBalance}'")
                    return

                print(f" - Proceeding with payment of '{payment}' because Alice's bank balance is: "
                      f"'{aliceBalance}'")

                # ARTIFICIAL PAUSE TO ENABLE THE RACE CONDITION OF TWO TRANSACTIONS TO OCCUR
                print(f" - Started sleeping for {SLEEP_SECS} seconds")
                time.sleep(SLEEP_SECS)
                print(f" - Finished sleeping")

                # PERFORM THE PAYMENT TRANSFER FROM ONE OF ALICE'S ACCOUNT TO ONE OF BOB'S ACCOUNTS
                acc_coll.update_one(
                    {
                        'account_holder': 'Alice',
                        'account_type': account_type
                    },
                    {
                        '$inc': {'balance': (payment * -1)}
                    },
                    session=tx_sess)
                acc_coll.update_one(
                    {
                        'account_holder': 'Bob',
                        'account_type': account_type
                    },
                    {
                        '$inc': {'balance': payment}
                    },
                    session=tx_sess)
    except Exception as e:
        print(f" - Conflict detected as expected, to prevent a payment of '{payment}' from causing "
              f"Alice to go overdrawn. Exception details: {e}")

    aliceBalance = getAliceCurrentBalance(None, acc_coll, False)

    if aliceBalance < Decimal(0):
        print(f" - OVERDRAWN ISSUE - Alice's balance overdrawn upon checking after the payment "
              f"attempt completed, with the checked bank balance being: {aliceBalance}")
    else:
        print(f" - Good result - Alice's balance is ok upon checking after the payment attempt "
              f"completed, with the checked bank balance being: {aliceBalance}")
