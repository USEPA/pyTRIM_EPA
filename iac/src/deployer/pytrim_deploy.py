import boto3
import getopt, json, sys
from common import die, whoami_aws, loggy
from helpers.cloudformation_helper import CloudFormationHelper
from helpers.beanstalk_helper import BeanstalkHelper
from helpers.cronjobs_helper import CronjobsHelper
from helpers.docker_helper import DockerHelper
from helpers.elastic_ip_helper import ElasticIpHelper
from helpers.ssh_keypair_helper import SshKeypairHelper

# inspired by / based on / rips off ~/development/epa_jira_automation/src/deployer.py
#tfeiler notes
#
#* uses local virtual environment "pytrim_deploy" (needs boto3)
#* before deploying call e.g. "aws_sso_login pytrim_dev" (if you're tfeiler) or assume valid credentials some other way (if you're not)

class PyTrimDeployer(object):
    def __init__(self, config_file, whoami):
        self.whoami = whoami
        with open(config_file, "r") as f:
            self.cfg = json.load(f)
            loggy(f"Stack: '{self.get_cfg_val('environment_name')}'")

    def run_deployment(self, mode):
        loggy(f"running deployment in mode '{mode}'")

        if mode == "full" or mode == "ssh_key":
            self.create_ssh_key_if_needed()

        if mode == "full" or mode == "elastic_ip":
            self.resolve_elastic_ip()

        if mode == "full" or mode == "cloudformation":
            self.do_cf_stack_work()

        if mode == "crons":
            self.create_cronjobs()

        if mode == "full" or mode == "docker":
            self.build_and_push_docker_images()

        if mode == "full" or mode == "push_flask_build":
            self.build_and_push_flask_app()

    def get_cfg_val(self, path, default_val = None):
        chunks = path.split(".")
        area_to_check = self.cfg
        for c in chunks:
            if c in area_to_check:
                area_to_check = area_to_check[c]
            else:
                return default_val
        return area_to_check

    def create_ssh_key_if_needed(self):
        ssh_keypair_name = self.get_cfg_val("aws.ssh_keypair_name")
        loggy(f"checking ssh keypair '{ssh_keypair_name}'")

        ssh_helper = SshKeypairHelper()
        keypair_data = ssh_helper.generate_keypair_if_needed(ssh_keypair_name)
        if keypair_data["status"] == "key created":
            loggy(f"Created ssh keypair '{ssh_keypair_name}' on AWS; stored locally at '{keypair_data['pem_path']}'", indent=1)
        elif keypair_data["status"] == "existing key found":
            loggy(f"Using pre-existing key '{ssh_keypair_name}'", indent=1)

    def resolve_elastic_ip(self):
        eip_name = self.get_cfg_val("aws.eip_name")
        loggy(f"checking elastic ip '{eip_name}'")

        helper = ElasticIpHelper()
        eip_allocation_id, is_currently_in_use = helper.find_or_create_eip(eip_name)
        loggy(f"'{eip_name}' --> '{eip_allocation_id}'", indent=1)

    def do_cf_stack_work(self):
        eip_name = self.get_cfg_val("aws.eip_name")
        cert_id = self.get_cfg_val("aws.webserver_certificate_id")
        env_name = self.get_cfg_val("environment_name")
        short_env_profile = self.get_cfg_val("short_env_profile")
        ssh_keypair_name = self.get_cfg_val("aws.ssh_keypair_name")
        vpc_seg = self.get_cfg_val("aws.cidr_segment_vpc")
        loggy(f"building AWS cloudformation stack named '{env_name}' / {vpc_seg}")

        # go from simple cert_id to fully qualified cert arn;
        # the config file gets something like "6f39535c-f167-4048-9304-6af9803a2498"
        # and we want:
        # "arn:aws:acm:us-east-1:426714360284:certificate/6f39535c-f167-4048-9304-6af9803a2498"
        sess = boto3.session.Session()
        web_server_cert_arn = f"arn:aws:acm:{sess.region_name}:{self.whoami['account']}:certificate/{cert_id}"

        # get the elastic allocation id
        eip_helper = ElasticIpHelper()
        (elastic_ip_allocation_id, is_already_allocated) = eip_helper.find_or_create_eip(eip_name)
        if elastic_ip_allocation_id is None:
            die(f"unable to find eip with name '{eip_name}'...")

        ingress_data = self.get_cfg_val("aws.ec2_ingress")

        # create mysql secret? We did this by hand on old PyTRIM account
        # but now it's part of the stack...but CF can be weird about bringing
        # in something that wasn't initially part of the stack. So we have this
        # KludgeDoSecret param we pass in that controls creation.
        #
        # logic is basically if the secret needs creating or is already part of
        # this stack, set it to true. Otherwise, set it to false.
        secret_client = boto3.client("secretsmanager")
        secret_kludge = "???"
        try:
            secret_probe = secret_client.describe_secret(SecretId="pytrim/database/credentials")
            stack_name_tag = next((x for x in secret_probe.get("Tags", []) if x["Key"] == "aws:cloudformation:stack-name"), None)
            stack_name = stack_name_tag["Value"] if stack_name_tag is not None else None

            if stack_name is not None:
                if stack_name == env_name:
                    # it's part of THIS stack 
                    secret_kludge = "true"
                else:
                    # it's part of ANOTHER stack (maybe we spun up a couple; hope they don't want separate passwords!)
                    secret_kludge = "false"
            else:
                # it's not part of any stack
                secret_kludge = "false"
        except:
            # secret doesn't exist at all
            secret_kludge = "true"

        cf_helper = CloudFormationHelper()
        cf_helper.create_or_update_stack(env_name, {
            "EnvironmentName": env_name,
            "KludgeDoSecret": secret_kludge,
            "ShortEnvironmentProfile": short_env_profile,
            "CidrSegmentVPC": vpc_seg,
            "WebServerCertArn": web_server_cert_arn,
            "DatabaseName": self.get_cfg_val("aws.db.dbname"),
            "DatabaseMasterAccountUsername": self.get_cfg_val("aws.db.username"),
            "DatabaseMasterAccountPassword": self.get_cfg_val("aws.db.password"),
            "BastionPassthroughKeyPairName": ssh_keypair_name,
            "NATGatewayElasticIPAllocationID": elastic_ip_allocation_id,
        }, ingress_data)

    def create_cronjobs(self):
        loggy(f"setting up cronjobs")
        crons = self.get_cfg_val("aws.crons")
        if not crons:
            loggy(f"Skipping...")
            return
        env_name = self.get_cfg_val("environment_name")
        crons_helper = CronjobsHelper()
        crons_helper.create_cronjobs(env_name, crons)

    def build_and_push_docker_images(self):
        loggy(f"DOCKER SETUP!")
        docker_helper = DockerHelper()
        env_name = self.get_cfg_val("environment_name")
        loggy(f"performing Docker build/deploy...")
        docker_helper.build_etc(env_name)

    def build_and_push_flask_app(self):
        beanstalk_helper = BeanstalkHelper()
        env_name = self.get_cfg_val("environment_name")
        loggy(f"performing Flask package/deploy")
        beanstalk_helper.build_etc(env_name)


def usage(msg=""):
    loggy(
        f"Usage: python ls_deploy.py -c <json_configuration_file> (-m <mode>) (-p <aws_profile_name>)"
    )
    die(msg)

if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "c:m:p:", [ "config=", "mode=", "profile=" ])
    except getopt.GetoptError as e:
        usage(e)

    config_file = None
    mode = None
    profile = None
    for opt, arg in opts:
        if opt in ("-c", "--config"):
            config_file = arg
        elif opt in ("-m", "--mode"):
            mode = arg
        elif opt in ("-p", "--profile"):
            profile = arg

    if mode is None:
        mode = "full"
    if profile:
        boto3.setup_default_session(profile_name=profile)


    if config_file is None:
        usage("No config supplied")
    else:
        # message the user so they are sure to be credentialed as proper user
        whoami = whoami_aws()
        loggy(f"Running PyTrim deployment script, mode '{mode}', as AWS userid '{whoami['user_id']}' on account '{whoami['account']}'")

        active_development_skip_confirmation_screen = False
        if active_development_skip_confirmation_screen:
            if whoami["account"] != "426714360284" and whoami["account"] != "736887025159":
                print(f"BAD ACCOUNT...")
                sys.exit(1)
            else:
                print(f"\n>>>>>>> DUMMY HARDCODE ALLOW THIS ACCOUNT ONLY DURING ACTIVE DEVELOPMENT CYCLE <<<<<<<<\n")
                proceed_or_not = "y"
        else:
            proceed_or_not = input("Proceed [y/n]? ")

        if proceed_or_not[0].lower() == "y":
            d = PyTrimDeployer(config_file, whoami)
            d.run_deployment(mode)
