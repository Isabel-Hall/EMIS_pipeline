import json
from pathlib import Path
from fhir.resources import construct_fhir_element
import fire
from tqdm import tqdm

def validate_resources(input_dir="", output_dir=""):
    # Create output directory
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    input_dir = Path(input_dir)
    input_filepaths = list(input_dir.glob("*.json"))

    # For each file in resources directory validate that they contain valid FHIR resources
    for p in tqdm(input_filepaths, total=len(input_filepaths)):

        # Open each json file containing a list of resources of a specific type
        with p.open(mode="r") as f:
            resource_list = json.load(f)
            output_path = output_dir / p.parts[1]
            invalid_output_path = output_dir / "invalid_resources.json"

        validated_resources = []
        invalid_resources = []

        for resource in resource_list:
            resource_type = resource["resource"]["resourceType"]

            # Validate that the resource has a valid FHIR resource type
            try:
                fhir_element = construct_fhir_element(resource_type, resource["resource"])

                validated_resources.append(resource)

            except ValueError:
                # If invalid will save it to a separate invalid resources file so it can be reviewed
                invalid_resources.append(resource)

        # Save the lists of valid and invalid resources to their respective files
        dump_to_file(output_path, validated_resources)
        if len(invalid_resources) > 0:
            dump_to_file(invalid_output_path, invalid_resources)



def dump_to_file(output_path, resources):
    """
    Takes a target file path and a list of resources
    Saves the resources to the file path, if the file already contains exists it will the extend the list of resources it contains
    """
    # load the target file if it already exists
    if output_path.exists():
        with output_path.open(mode="r") as f:
            records = json.load(f)

        records.extend(resources)

    else:
        records = resources

    # Save the new/updated list as a json file
    with output_path.open(mode="w") as f:
        json.dump(records, f)


if __name__ == "__main__":
    fire.Fire(validate_resources)