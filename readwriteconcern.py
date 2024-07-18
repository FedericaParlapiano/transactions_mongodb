from pymongo import MongoClient, WriteConcern
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import ReadPreference
from pymongo.errors import PyMongoError, WriteConcernError

connection_string = "mongodb+srv://arianna:arianna@cluster0.o61ssco.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

client = MongoClient(connection_string)


# Step 1: Define the callback that specifies the sequence of operations to perform inside the transactions.
def callback(session, account_id=None, new_account_id=None):
    # Get reference to 'accounts' collection
    accounts_collection = session.client.sample_analytics.accounts.with_options(
        write_concern=WriteConcern(w=1, j=True)
    )

    # Get reference to 'customers' collection
    customers_collection = session.client.sample_analytics.customers.with_options(
        write_concern=WriteConcern(w=1, j=True)
    )

    # Transaction operations
    # Important: You must pass the session to each operation

    # Update sender account: update account ID
    accounts_collection.update_one(
        {"account_id": account_id},
        {"$set": {"account_id": new_account_id}},
        session=session,
    )

    # Update customer account: update account ID in the customer's account list
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
        121212,
        278603
    )


# Step 2: Start a client session with write concern, read concern, and read preference
with client.start_session() as session:
    try:
        # Step 3: Use with_transaction to start a transaction, execute the callback, and commit (or cancel on error)
        session.with_transaction(
            callback_wrapper,
            write_concern=WriteConcern(w=1, j=True)
        )
    except (PyMongoError) as exc:
        print(f"Transaction failed: {exc}")

primary_result = client.sample_analytics.accounts.with_options(
    read_preference=ReadPreference.PRIMARY
).find_one({"account_id": 278603})

print(f"Primary read result: {primary_result}")

secondary_result = client.sample_analytics.accounts.with_options(
    read_preference=ReadPreference.SECONDARY
).find_one({"account_id": 278603})

print(f"Secondary read result: {secondary_result}")

client.close()
