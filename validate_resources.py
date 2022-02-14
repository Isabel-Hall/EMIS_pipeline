import json
from pathlib import Path
from fhir.resources import construct_fhir_element

# Create output directory
output_dir = Path("validated_resources")
if not output_dir.exists():
    output_dir.mkdir()

input_dir = Path("resources")

# For each file in resources directory validate that they contain valid FHIR resources
for p in input_dir.iterdir():
    #print(p)

    with p.open(mode="r") as f:
        resource_list = json.load(f)
        #print(len(resource_list))

        for resource in resource_list:
            resource_type = resource["resource"]["resourceType"]

            # Validate that the resource has a valid FHIR resource type
            try:
                fhir_element = construct_fhir_element(resource_type, resource["resource"])

                # Save the validated records to a new json file
                output_path = output_dir / p.parts[1]
                
                if output_path.exists():
                    with output_path.open(mode="r") as f:
                        records = json.load(f)

                    records.append(resource)

                else:
                    records = [resource]

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