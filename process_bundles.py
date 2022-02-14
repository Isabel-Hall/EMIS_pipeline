import json
from pathlib import Path
import fire


def process_bundles(dir_path):
    """
    Takes an directory of json files containing FHIR data
    Separates it based on resource types and saves these into json files
    """
    input_dir = Path(dir_path)
    for p in input_dir.iterdir():
        print("opening file:", p)
        # Open the FHIR json file
        with p.open(mode="r") as f:
            bundle = json.load(f)
            entries = bundle["entry"]


        resource_types = set()

        # Make a directory to save the processed files
        output_dir = Path("resources")
        if not output_dir.exists():
            output_dir.mkdir()

        # Group different resource types together and save them into distinct json files
        for resource in entries:
            resource_type = resource["resource"]["resourceType"]
            resource_types.add(resource_type)
            resource_file_path = output_dir / f"{resource_type}.json"

            if resource_file_path.exists():

                # get existing records of this resource
                with resource_file_path.open(mode="r") as f:
                    records = json.load(f)
            
                # add stuff to it
                records.append(resource)

            else:
                records = [resource]
                
            # save it to disk
            with resource_file_path.open(mode="w") as f:
                json.dump(records, f)

        #print(resource_types)

if __name__ == "__main__":
    fire.Fire(process_bundles)