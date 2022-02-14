import json
from pathlib import Path

with open("/home/issie/code/exa-data-eng-assessment/data/Aaron697_Dickens475_8c95253e-8ee8-9ae8-6d40-021d702dc78e.json", "r") as f:
    bundle = json.load(f)
    entries = bundle["entry"]
print(len(entries))

resource_types = set()
output_dir = Path("resources")
if not output_dir.exists():
    output_dir.mkdir()


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
        
    # save it back to disk
    with resource_file_path.open(mode="w") as f:
        json.dump(records, f)



print(resource_types)