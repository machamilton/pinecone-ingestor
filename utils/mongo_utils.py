from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient

def ConnectAndInsertData(
    ssh_host="3.139.87.32",
    ssh_user="ubuntu",
    ssh_key_path="D:\\Users\\Gabriel\\Desktop\\GIT\\pinecone-ingestor\\mongo-server-key.pem",
    mongo_user="admin",
    mongo_password="",
    db_name="mydatabase",
    collection_name="mycollection",
    data=None
):
    with SSHTunnelForwarder(
        (ssh_host, 22),
        ssh_username=ssh_user,
        ssh_private_key=ssh_key_path,
        remote_bind_address=('127.0.0.1', 27017),
        local_bind_address=('localhost', 27018)  # você pode escolher outra porta local
    ) as tunnel:

        mongo_uri = f"mongodb://{mongo_user}:{mongo_password}@localhost:{tunnel.local_bind_port}"
        client = MongoClient(mongo_uri)
        collection = client[db_name][collection_name]

        if data:
            if isinstance(data, list):
                result = collection.insert_many(data)
                print(f"✅ Inserted {len(result.inserted_ids)} documents.")
            else:
                result = collection.insert_one(data)
                print(f"✅ Inserted document with _id: {result.inserted_id}")
        else:
            print("📂 Collections:", client[db_name].list_collection_names())

        client.close()
