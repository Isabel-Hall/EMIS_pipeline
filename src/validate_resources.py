import json
from pathlib import Path
from fhir.resources import construct_fhir_element
import fire

def validate_resources(input_dir="", output_dir=""):
# Create output directory
    output_dir = Path(output_dir)
    if not output_dir.exists():
        output_dir.mkdir()

    input_dir = Path(input_dir)

    # For each file in resources directory validate that they contain valid FHIR resources
    for p in input_dir.glob("*.json"):

        # Open each json file containing a list of resources of a specific type
        with p.open(mode="r") as f:
            resource_list = json.load(f)


            for resource in resource_list:
                resource_type = resource["resource"]["resourceType"]

                # Validate that the resource has a valid FHIR resource type
                try:
                    fhir_element = construct_fhir_element(resource_type, resource["resource"])

                    # Save the validated records to a new json file
                    output_path = output_dir / p.parts[1]
                    
                    # load the target file if it already exists
                    if output_path.exists():
                        with output_path.open(mode="r") as f:
                            records = json.load(f)

                        records.append(resource)

                    else:
                        records = [resource]

                    # Save the updated json file, containing only valid FHIR resources
                    with output_path.open(mode="w") as f:
                        json.dump(records, f)


                except ValueError:
                    # If invalid will save it to a separate invalid resources file so it can be reviewed
                    invalid_path_file = output_dir / "invalid_resources.json"

                    if invalid_path_file.exists():
                        with invalid_path_file.open(mode="r") as f:
                            records = json.load(f)

                        records.append(resource)

                    else:
                        records = [resource]

                    with invalid_path_file.open(mode="w") as f:
                        json.dump(records, f)

if __name__ == "__main__":
    fire.Fire(validate_resources)