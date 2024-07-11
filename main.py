from pymongo import MongoClient


def get_database():
    CONNECTION_STRING = "mongodb+srv://federica:federica@cluster1.1mnlttb.mongodb.net/?appName=mongosh+2.2.10"

    client = MongoClient(CONNECTION_STRING)

    return client['sample_training']


if __name__ == "__main__":
    # Get the database
    dbname = get_database()

    comments_collections = dbname["comments"]

    item_details = comments_collections.find()

    print(comments_collections)

