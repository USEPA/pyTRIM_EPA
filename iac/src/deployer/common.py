import boto3, os, sys, pprint, re, time
from datetime import datetime

MAX_NUM_AWAIT_ATTEMPTS = 50
STACK_CREATION_SLEEP_AMOUNT = 30

# this takes ~6 minutes as of 2023-02-10 with a t2.micro instance
# this is for an AWS CLoudFormation stack...
def await_stack_completion(stack_name):
    cf_client = boto3.client("cloudformation")
    for i in range(0, MAX_NUM_AWAIT_ATTEMPTS):
        loggy(f"attempt #{i+1} of {MAX_NUM_AWAIT_ATTEMPTS} awaiting stack completion for stack '{stack_name}'...", indent=1)

        try:
            stack_response = cf_client.describe_stacks(StackName=stack_name)
            stacks = stack_response.get("Stacks", [])

            if len(stacks) > 1:
                die(f"multiple ({len(stacks)}) CloudFormation stacks with name '{stack_name}' found; cannot proceed")
            elif len(stacks) == 0:
                loggy(f"\tno stack with name '{stack_name}' found...", indent=1)
            else:
                stack = stacks[0]
                stack_id = stack.get("StackId")
                stack_status = stack.get("StackStatus")
                outputs = stack.get("Outputs")

                if stack_status == "CREATE_COMPLETE" or stack_status == "UPDATE_COMPLETE":
                    loggy(f"\tstack '{stack_name}' / '{stack_id}' is complete; proceeding", indent=1)
                    return (stack_id, outputs)
                elif stack_status == "CREATE_IN_PROGRESS":
                    loggy(f"\tstack creation still in progress...", indent=1)
                elif stack_status == "UPDATE_IN_PROGRESS":
                    loggy(f"\tstack update still in progress...", indent=1)
                elif stack_status == "ROLLBACK_COMPLETE":
                    die(f"\tstack creation rolled back due to an error; check AWS CloudFormation console for details...")
                else:
                    loggy(f"\tstack status now {stack_status}; not sure how to proceed...", indent=1)
        except:
            loggy(f"\tno stack with name '{stack_name}' found...", indent=1)

        loggy(f"\tsleeping for '{STACK_CREATION_SLEEP_AMOUNT}' seconds; will retry again then", indent=1)
        time.sleep(STACK_CREATION_SLEEP_AMOUNT)

def pp(x):
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(x)

# thanks https://github.com/mahmoudadel2/pysed/blob/master/pysed.py
def hotswap(find_text, replace_text, file_path):
    # print(f"HOTSWAP [{find_text}] -> [{replace_text}] in {file_path}")
    lines = []
    with open(file_path) as f:
        x = 0
        for item in f:
            newitem = re.sub(find_text, replace_text, item)
            lines.append(newitem)
            x += 1

    with open(file_path, "w") as f:
        f.truncate()
        for line in lines: f.writelines(line)

def loggy(x, indent=0):
    now = datetime.now()
    stamp = now.strftime('%Y-%m-%d %H:%M')
    indention = indent * "\t" if indent > 0 else " "
    print(f"[{stamp}]{indention}{x}")

# get the root of the deployment project; e.g. /Users/tfeiler/development/trim-builder/iac/
def figure_home_dir():
    d = os.path.dirname(__file__)

    # lose trailing directory marker
    if d[-1] == os.path.sep:
        d = d[:-1]

    # lose leading directory marker
    if d[0] == os.path.sep:
        d = d[1:]

    chunks = d.split(os.path.sep)
    return os.path.sep + os.path.sep.join(chunks[0:-2]) + os.path.sep

# get the root of the entire PyTrim project; e.g. /Users/tfeiler/development/trim-builder/
def figure_parent_dir():
    d = os.path.dirname(__file__)

    # lose trailing directory marker
    if d[-1] == os.path.sep:
        d = d[:-1]

    # lose leading directory marker
    if d[0] == os.path.sep:
        d = d[1:]

    chunks = d.split(os.path.sep)
    return os.path.sep + os.path.sep.join(chunks[0:-3]) + os.path.sep

def whoami_aws():
    sts_client = boto3.client("sts")
    identity = sts_client.get_caller_identity()
    user_id = identity["UserId"]
    account = identity["Account"]

    return {
        "user_id": user_id,
        "account": account
    }

def die(msg):
    print(f"FATAL ERROR: {msg}")
    sys.exit(1)

def extract_output_val(outputs, key, default_val = None):
    first_matching_el = next(iter([x for x in outputs if x["OutputKey"] == key]), None)
    return first_matching_el.get("OutputValue") if first_matching_el is not None else default_val

def await_beanstalk_app_deployment(stack_name):
    eb_client = boto3.client("elasticbeanstalk")
    for i in range(0, MAX_NUM_AWAIT_ATTEMPTS):
        loggy(f"attempt #{i+1} of {MAX_NUM_AWAIT_ATTEMPTS} awaiting app deployment for stack '{stack_name}'...", indent=1)

        try:
            # print(f"APPS:")
            # app_response = eb_client.describe_applications(ApplicationNames=[stack_name])
            # print(app_response)

            # print("####")

            # print("ENVS:")
            env_response = eb_client.describe_environments(ApplicationName=stack_name, EnvironmentNames=[f"{stack_name}-web"])
            # print(env_response)
            web_env = env_response.get("Environments", [{}])[0]
            # print(f"~~~~~ {web_env}")
            status = web_env.get("Status")
            health = web_env.get("Health")
            abortable = web_env.get("AbortableOperationInProgress")
            health_status = web_env.get("HealthStatus")
            if status == "Ready" and health == "Green" and abortable == False and health_status == "Ok":
                loggy(f"\tapp deployment for stack '{stack_name}' is complete; proceeding", indent=1)
                return
            else:
                loggy(f"\tapp deployment still underway: {status=}, {health=}, {abortable=}, {health_status=}")
        except Exception as e:
            loggy(e)

        loggy(f"\tsleeping for '{STACK_CREATION_SLEEP_AMOUNT}' seconds; will retry again then", indent=1)
        time.sleep(STACK_CREATION_SLEEP_AMOUNT)
