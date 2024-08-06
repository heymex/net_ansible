import json
import yaml
import argparse

def main(input_file, output_file):
    # Read the JSON data from the input file
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Transform data to the desired format
    yaml_data = {
        "hosts": "*",
        "gather_facts": "no",
        "tasks": [
            {
                "name": "Deploy standard VLANs to edge devices",
                "cisco.ios.ios_vlans": {
                    "config": [
                        {
                            "name": item["name"],
                            "vlan_id": item["vlan_id"],
                            "state": item["state"],
                            "shutdown": item["shutdown"],
                            "mtu": item["mtu"]
                        } for item in data["gathered"]
                    ]
                }
            }
        ]
    }
    
    # Convert to YAML
    yaml_output = yaml.dump([yaml_data], default_flow_style=False)
    
    # Write the YAML output to the output file
    with open(output_file, 'w') as f:
        f.write(yaml_output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON to YAML.')
    parser.add_argument('input_file', type=str, help='The input JSON file')
    parser.add_argument('output_file', type=str, help='The output YAML file')
    
    args = parser.parse_args()
    main(args.input_file, args.output_file)