import pymongo
import os
import json
from pathlib import Path
from tqdm import tqdm
import fire

class createDB():

    def __init__(self):
        # Initialise a mongoDB client
        mongo_url = os.environ["MONGO_URL"]
        mongo_username = os.environ["MONGO_INITDB_ROOT_USERNAME"]
        mongo_password = os.environ["MONGO_INITDB_ROOT_PASSWORD"]
        client = pymongo.MongoClient(
            mongo_url,
            username=mongo_username,
            password=mongo_password
        )
        self.db = client.fhir_data
        

    def add_collection(self, file_path):

        # Open a json file containing fhir resources, of one resource type

        with file_path.open(mode="r") as f:
            resources = json.load(f)

        records_to_save = []

        # Extract the resource data and add the fullUrl, removes one layer of nesting
        for resource in resources:
            res = resource["resource"]
            url = resource["fullUrl"]
            res["fullUrl"] = url
            records_to_save.append(res)
        
        # Insert into mongoDB client
        name = file_path.stem
        inserted = self.db[name].insert_many(records_to_save)
        return inserted

    def add_many_collections(self, path_dir):
        path = Path(path_dir)
        file_paths = list(path.glob("*.json"))
        for p in tqdm(file_paths, total = len(file_paths)):
            inserted = self.add_collection(p)


if __name__ == "__main__":
    #db = get_db_details()
    #file_path = "../validated_resources/"

    fire.Fire(createDB)