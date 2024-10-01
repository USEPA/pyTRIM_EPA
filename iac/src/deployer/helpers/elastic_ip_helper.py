import boto3, getopt, os, sys
from common import die, figure_home_dir, whoami_aws, loggy

# either looks up or creates an elastic ip with the specified name.

class ElasticIpHelper(object):
    def __init__(self):
        pass

    def find_or_create_eip(self, name):
        ec2_client = boto3.client("ec2")

        response = ec2_client.describe_addresses(
            Filters=[ { 'Name': 'tag:Name', 'Values': [ name ] } ]
        )

        addresses = response.get("Addresses", [])

        if len(addresses) == 0:
            loggy(f"No elastic IP found with name '{name}'; attempting creation...", indent=1)
            address = ec2_client.allocate_address(
                Domain='vpc',
                TagSpecifications=[
                    {
                        "ResourceType":"elastic-ip",
                        "Tags":[
                            {
                                "Key": "Name",
                                "Value": name
                            }
                        ]
                    }
                ],
            )
            loggy(address, indent=1)
            allocation_id = address.get("AllocationId")
            return (allocation_id, False)
        elif len(addresses) == 1:
            address = addresses[0]
            association_id = address.get("AssociationId")
            allocation_id = address.get("AllocationId")
            if association_id is None:
                loggy(f"Found existing available elastic IP '{name}' with allocation id '{allocation_id}'", indent=1)
                return (allocation_id, False)
            else:
                return (allocation_id, True)
        else:
            die("Multiple elastic IPs found with name '{name}'; cannot determine which to proceed with")

    """
    def find_or_create_eip(self, name):
        ec2_client = boto3.client("ec2")

        response = ec2_client.describe_addresses(
            Filters=[ { 'Name': 'tag:Name', 'Values': [ name ] } ]
        )

        addresses = response.get("Addresses", [])

        if len(addresses) == 0:
            loggy(f"No elastic IP found with name '{name}'; attempting creation...", indent=1)
            address = ec2_client.allocate_address(
                Domain='vpc',
                TagSpecifications=[
                    {
                        "ResourceType":"elastic-ip",
                        "Tags":[
                            {
                                "Key": "Name",
                                "Value": name
                            }
                        ]
                    }
                ],
            )
            loggy(address, indent=1)
            allocation_id = address.get("AllocationId")
            return allocation_id
        elif len(addresses) == 1:
            address = addresses[0]
            association_id = address.get("AssociationId")
            if association_id is None:
                allocation_id = address.get("AllocationId")
                loggy(f"Found existing available elastic IP '{name}' with allocation id '{allocation_id}'", indent=1)
                return allocation_id
            else:
                die(f"elastic ip '{name}' was found but already had an allocation id; unable to proceed.")
        else:
            die("Multiple elastic IPs found with name '{name}'; cannot determine which to proceed with")

    def find_existing_available_eip(self, name):
        ec2_client = boto3.client("ec2")

        response = ec2_client.describe_addresses(
            Filters=[ { 'Name': 'tag:Name', 'Values': [ name ] } ]
        )

        addresses = response.get("Addresses", [])

        if len(addresses) == 0:
            return None
        elif len(addresses) == 1:
            address = addresses[0]
            association_id = address.get("AssociationId")
            if association_id is None:
                allocation_id = address.get("AllocationId")
                loggy(f"Found existing available elastic IP '{name}' with allocation id '{allocation_id}'", indent=1)
                return allocation_id
            else:
                die(f"elastic ip '{name}' was found but already had an allocation id; unable to proceed.")
        else:
            die("Multiple elastic IPs found with name '{name}'; cannot determine which to proceed with")
    """
