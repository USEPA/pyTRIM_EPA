import boto3, getopt, os, sys
from common import figure_home_dir, whoami_aws

# creates an ssh keypair with the specified name (if it doesn't already exist); saves it to appropriate location

class SshKeypairHelper(object):
    def __init__(self):
        pass

    def generate_keypair_if_needed(self, name):
        ec2_client = boto3.client("ec2")

        # check to see if a key wit this name already exists on AWS...if so, we'll use it
        key_exists_on_aws = False
        existing_pairs = ec2_client.describe_key_pairs()
        for pair in existing_pairs["KeyPairs"]:
            if name == pair["KeyName"]:
                key_exists_on_aws = True

        if key_exists_on_aws:
            return { "status": "existing key found", "pem_path": None }

        # setup directory storage etc.
        project_home_dir = figure_home_dir()
        key_storage_dir = project_home_dir + "output" + os.path.sep + "ssh_key"
        key_file_location = key_storage_dir + os.path.sep + name + ".pem"
        
        if not os.path.exists(key_storage_dir):
           os.makedirs(key_storage_dir)

        # talk to ec2 and make the keypair...
        keypair_response = ec2_client.create_key_pair(KeyName=name)

        # save it locally...
        with open(key_file_location, "w") as private_key_file:
            private_key_file.write(keypair_response["KeyMaterial"])

        # set appropriate perms...
        os.chmod(key_file_location , 0o400)

        # and message the user
        return { "status": "key created", "pem_path": key_file_location }

"""
if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "n:", [ "name=" ])
    except getopt.GetoptError:
        usage()

    key_pair_name = None
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            key_pair_name = arg

    if key_pair_name is None:
        print(f"Usage: python create_ssh_keypair.py -n <name>")
    else:
        # message the user so they are sure to be credentialed as proper user
        whoami = whoami_aws()
        print(f"creating keypair '{key_pair_name}' as AWS userid '{whoami['user_id']}' on account '{whoami['account']}'")
        proceed_or_not = input("Proceed [y/n]? ")

        if proceed_or_not[0].lower() == "y":
            kpg = SshKeypairGenerator()
            output_loc = kpg.generate_keypair_if_needed(key_pair_name)
            print(f"Keyfile with name '{key_pair_name}' created on AWS; saved locally to '{output_loc}'")
"""
