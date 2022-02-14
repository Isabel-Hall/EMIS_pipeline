import json
from pathlib import Path
from fhir.resources.patient import Patient
from fhir.resources import construct_fhir_element

# Create output directory
output_dir = Path("validated_resources")
if not output_dir.exists():
    output_dir.mkdir()

input_dir = Path("resources")

# For each file in resources directory validate that they contain valid FHIR resources
for p in input_dir.iterdir():


    with open(p, "r") as f:
        resource_list = json.load(f)

        for resource in resource_list:
            resource_type = resource["resource"]["resourceType"]

            try:
                fhir_element = construct_fhir_element(resource_type, resource["resource"])
            except ValueError:
                