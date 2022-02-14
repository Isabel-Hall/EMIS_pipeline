import pymongo
import os
import json
from pathlib import Path

def get_db_details():
    mongo_url = os.environ["MONGO_URL"]
    mongo_username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
    mongo_password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
    client = pymongo.MongoClient(
        mongo_url,
        username=mongo_username,
        password=mongo_password
    )
    db = client.fhir_data
    return db

def add_patients(db, file_path):
    path = Path(file_path)
    with path.open(mode="r") as f:
        resources = json.load(f)

    items_to_save = []

    for resource in resources:
        res = resource["resource"]
        url = resource["fullUrl"]
        res["fullUrl"] = url
        items_to_save.append(res)
    
    name = path.stem
    inserted = db[name].insert_many(items_to_save)

    pats = list(db[name].find({}))
    print(pats[0])

if __name__ == "__main__":
    db = get_db_details()
    file_path = "../validated_resources/Patient.json"

    add_patients(db, file_path)