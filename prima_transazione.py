# Connect to MongoDB cluster with MongoClient
from pymongo import MongoClient

connection_string = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"

client = MongoClient(connection_string)

# Step 1: Define the callback that specifies the sequence of operations to perform inside the transactions.
def callback(session, account_id=None, new_account_id=None):

    # Get reference to 'accounts' collection
    accounts_collection = session.client.sample_analytics.accounts

    # Get reference to 'transfers' collection
    customers_collection = session.client.sample_analytics.customers


    # Transaction operations
    # Important: You must pass the session to each operation

    # Update sender account: subtract transfer amount from balance and add transfer ID
    accounts_collection.update_one(
        {"account_id": account_id},
        {"$set": {"account_id": new_account_id}},
        session=session,
    )

    # Update receiver account: add transfer amount to balance and add transfer ID
    customers_collection.update_one(
        {"accounts": {"$in": [account_id]}},
        {"$set": {"accounts.$": new_account_id}},
        session=session,
    )

    print("Transaction successful")

    return


def callback_wrapper(s):
    callback(
        s,
        987709,
        121212
    )


# Step 2: Start a client session
with client.start_session() as session:
    # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or cancel on error)
    session.with_transaction(callback_wrapper)


client.close()