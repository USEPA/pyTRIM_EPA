import boto3, getopt, os, sys
from common import await_stack_completion, figure_home_dir, whoami_aws, die, loggy

class CloudFormationHelper(object):
    def __init__(self):
        pass

    def prep_params(self, params):
        return [ {"ParameterKey": t[0], "ParameterValue": str(t[1]) } for t in [ (k, v) for k, v in params.items() ] ]

    def insert_dynamic_content(self, dynamic_section_name, line_storage):
        loggy(f"insert dynamic '{dynamic_section_name}' contents...", indent=1)

        # these are just one-off hardcoded things; if we end up needing a lot of them let's rethink...
        # for right now a real templating system is just overkill.
        if dynamic_section_name == "ec2_ingress":
            # allowable_ips = [ ("tfeiler home IP", "66.188.191.91/32"), ("goobar", "0.0.0.0/0") ]

            for entry in self.ingress_data:
                indent = " " * 8
                line_storage.append(f"{indent}-\n")
                indent = " " * 10
                line_storage.append(f"{indent}CidrIp: {entry['cidr']}\n")
                line_storage.append(indent + "Description: !Sub 'ssh access to the ec2 instance in the ${EnvironmentName} VPC from " + entry['description'] + "'\n")
                line_storage.append(f"{indent}FromPort: 22\n")
                line_storage.append(f"{indent}ToPort: 22\n")
                line_storage.append(f"{indent}IpProtocol: tcp\n")


    # some things CloudFormation can't do - like loops. So we will now do a small bit of work
    # to get around this for things like "we want to specify an unknown # of IP's to get access to the
    # EC2 instance security group ingress"...
    def build_template(self, template_name):
        sep = os.path.sep

        PROJECT_HOME_DIR = figure_home_dir()

        # first load the template as-is...
        template_file_location = f"{PROJECT_HOME_DIR}src{sep}cloudformation{sep}{template_name}"

        with open(template_file_location, "r") as f:
            input_lines = f.readlines()

            dynamic_section_tracker = []
            fixed_lines = []
            for l in input_lines:
                if l.startswith("#START_DYNAMIC_SECTION"):
                    dynamic_section_name = l.replace("#START_DYNAMIC_SECTION", "").strip().replace("\n", "")
                    dynamic_section_tracker.append(dynamic_section_name)
                elif l.startswith("#END_DYNAMIC_SECTION"):
                    try:
                        last_section_name = dynamic_section_tracker.pop()
                    except:
                        last_section_name = None
                    dynamic_section_name = l.replace("#END_DYNAMIC_SECTION", "").strip().replace("\n", "")

                    if last_section_name == dynamic_section_name:
                        self.insert_dynamic_content(dynamic_section_name, fixed_lines)
                    else:
                        die("improperly nested dynamic sections in the template")

                if len(dynamic_section_tracker) == 0 and not l.startswith("#END_DYNAMIC_SECTION"):
                    fixed_lines.append(l)

        # uncomment these if you want to view the transformed template...
        """
        i = 1
        for l in fixed_lines:
            print(f"[{i}] {l}", end="")
            i += 1
        """

        return "".join(fixed_lines)

    # returns tuple - (does-stack-exist, if-so-whats-the-status)
    def check_stack(self, stack_name):
        try:
            print(f"CHECKING ON STACK '{stack_name}'...")
            stack_response = self.cf_client.describe_stacks(StackName=stack_name)
            stacks = stack_response.get("Stacks", [])

            if len(stacks) > 1:
                die(f"multiple ({len(stacks)}) CloudFormation stacks with name '{stack_name}' found; cannot proceed")
            elif len(stacks) == 0:
                # stack doesn't exist
                return ( False, None, None )
            else:
                stack = stacks[0]
                return ( True, stack.get("StackId"), stack.get("StackStatus") )
        except:
            # stack doesn't exist
            return ( False, None, None )

    def check_vpcs(self, cidr_segment):
        ec2_client = boto3.client("ec2")
        vpc_response = ec2_client.describe_vpcs(Filters=[
            {
                "Name": "cidr",
                "Values": [
                    f"10.{cidr_segment}.0.0/16"
                ]
            }
        ])

        for vpc in vpc_response.get("Vpcs", []):
            vpc_name_tag = next((x for x in vpc.get("Tags", []) if x["Key"] == "Name"), None)
            vpc_name = vpc_name_tag["Value"] if vpc_name_tag is not None else "(unnamed)"

            die(f"Cannot use config value 'cidr_segment_vpc': {cidr_segment}; CidrBlock 10.{cidr_segment}.0.0/16 already in use by existing VPC '{vpc.get('VpcId')}'/'{vpc_name}'")

    def create_or_update_stack(self, stack_name, params, ingress_data):
        aws_params = self.prep_params(params)

        self.cf_client = boto3.client("cloudformation")

        existing_stack_data = self.check_stack(stack_name)
        """
        if existing_stack_data[0] == True:
            loggy(f"stack {existing_stack_data[1]} already exists with name {stack_name}, status '{existing_stack_data[2]}'; not doing any work", indent=1)
            return existing_stack_data[1]
        else:

            # TODO - does this stack already exist? If so maybe we should try to recreate/update?

            self.check_vpcs(params["CidrSegmentVPC"])

            self.ingress_data = ingress_data

            template_contents = self.build_template("pytrim.yaml")

            response = self.cf_client.create_stack(
                StackName=stack_name,
                TemplateBody=template_contents,
                Parameters=aws_params,
                Capabilities=[ "CAPABILITY_IAM" ],
            )

            loggy(f"CREATION RESULT:", indent=1)
            loggy(response, indent=1)

            (stack_id, outputs) = await_stack_completion(stack_name)
            print(f"ALL DONE: {stack_id=}, {outputs=}")
        """

        if existing_stack_data[0] != True:
            # if creating, make sure the segment isn't already in use...
            self.check_vpcs(params["CidrSegmentVPC"])

        self.ingress_data = ingress_data

        template_contents = self.build_template("pytrim.yaml")

        create_or_update_method = None
        if existing_stack_data[0] == False:
            create_or_update_method = self.cf_client.create_stack
        else:
            create_or_update_method = self.cf_client.update_stack

        try:
            response = create_or_update_method(
                StackName=stack_name,
                TemplateBody=template_contents,
                Parameters=aws_params,
                Capabilities=[ "CAPABILITY_IAM" ],
            )

            loggy(f"CREATION/UPDATE RESULT:", indent=1)
            loggy(response, indent=1)
        except Exception as e:
            if "No updates are to be performed" in str(e):
                print(f"No updates needed for stack '{stack_name}'...")
            else:
                die(e)

        (stack_id, outputs) = await_stack_completion(stack_name)
        print(f"ALL DONE: {stack_id=}, {outputs=}")

