import json
from pathlib import Path
import fire
from tqdm import tqdm
from collections import defaultdict


def process_bundles(input_dir="", output_dir=""):
    """
    Takes an directory of json files containing FHIR data
    Separates it based on resource types and saves these into json files
    """
    input_dir = Path(input_dir)

    # Make a directory to save the processed files
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    input_filepaths = list(input_dir.glob("*.json"))

    for p in tqdm(input_filepaths, total=len(input_filepaths)):
        print("opening file:", p)
        # Open the FHIR json file
        with p.open(mode="r") as f:
            bundle = json.load(f)
            entries = bundle["entry"]


        resource_types = set()
        entry_resources = defaultdict(list)

        # Group different resource types together and save them into distinct json files
        for resource in entries:
            resource_type = resource["resource"]["resourceType"]
            resource_types.add(resource_type)
            resource_file_path = output_dir / f"{resource_type}.json"
            entry_resources[resource_file_path].append(resource)

        
        for resource_file_path, resources in entry_resources.items():

            if resource_file_path.exists():

                # get existing records of this resource
                with resource_file_path.open(mode="r") as f:
                    records = json.load(f)
            
                # add stuff to it
                records.extend(resources)

            else:
                records = resources
                
            # save it to disk
            with resource_file_path.open(mode="w") as f:
                json.dump(records, f)

        #print(resource_types)

if __name__ == "__main__":
    fire.Fire(process_bundles)