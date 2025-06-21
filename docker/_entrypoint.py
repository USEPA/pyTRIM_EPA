import json, os, sys

import uuid as uuidlib

from datetime import datetime as dt

import boto3

print(f"QUICK SHIM START - retrieve from secrets manager and set environment variables on the fly...")

print(f"MAKE SECRET CLiENT...")
secrets_client = boto3.client('secretsmanager')
print(f"got if: {secrets_client}")

response = secrets_client.get_secret_value(
    SecretId='pytrim/mysql'
)

print(f"secrets response: {response}")
secret_data = json.loads(response['SecretString'])

sqlalchemy_uri = f"mysql+pymysql://{secret_data['username']}:{secret_data['password']}@{os.environ.get('RDS_HOSTNAME')}:{os.environ.get('RDS_PORT')}/{os.environ.get('RDS_DB_NAME')}"

# put stuff into environment variables...
os.environ["RDS_USERNAME"] = secret_data["username"]
os.environ["RDS_PASSWORD"] = secret_data["password"]
os.environ["SQLALCHEMY_DATABASE_URI"] = sqlalchemy_uri



"""
# verify what's in the environment
print(f"ENVIRONMENT (start):")
for key, value in os.environ.items():
    print(f'{key}: {value}')
print(f"ENVIRONMENT (end):")
"""

print(f"QUICK SHIM END!")

from trim_core.algorithms.full_model_run import run_full_model
from trim_db import ScenarioService
from trim_frontend import create_app

"""
>>>>> WHEN TESTING LOCALLY <<<<<
    1. prep the Docker copy of the source code by running the following within an appropriate virtual env:

       cd <PROJECT_ROOT/docker && ./prepare_dockerized_pytrim.py

    2. run locally with a command like:

        TASK_TOKEN_ENV_VARIABLE=IGNOREME MYSQLPASSWORD= FLASK_DEBUG=development TRIM_SCENARIO_ID=2 python temp/docker_entrypoint.py

    If you're running in Vim/tmux like Tom does this might be helpful:

    map <BS> :call SendFreshCommandToTMUX("./prepare_dockerized_pytrim.py", "1")<enter>


    # -u switch makes python flush the output buffer as it runs; much easier to monitor what's going on...
    map \ :call SendFreshCommandToTMUX("TASK_TOKEN_ENV_VARIABLE=IGNOREME MYSQLPASSWORD= FLASK_DEBUG=development TRIM_SCENARIO_ID=2 python -u temp/docker_entrypoint.py \| tee /Users/tfeiler/development/trim-builder/unsynced/test.log", "1")<enter>

 

>>>>> WHEN RUNNING IN LOCAL DOCKER CONTAINER <<<<<
    (todo)

>>>>> WHEN RUNNING IN AWS ECS <<<<<
    (todo)
"""

# see https://stackoverflow.com/questions/68112428/input-and-ouput-to-ecs-task-in-step-function
# task definition is where we can define things like # of cpu's / memory. If we need to do e.g. GPU
#      we'd need to do EC2 instead of Fargate. Punting on that for now; next steps are:
# 1. get this working on pytrim aws account
# 2. get things spun up via CLoudFormation / deployment script. Wil need connectivity tothe pytrim db.
# 3. write a small entry wrapper (takes e.g. a senarioId) that then calls the real run_model stuff.

INCOMING_TOKEN_ENV_KEY = "TASK_TOKEN_ENV_VARIABLE"
STORAGE_BUCKET_NAME_KEY = "STORAGE_BUCKET_NAME"
SCENARIO_ID_KEY = "TRIM_SCENARIO_ID.$"
FAKE_KEY = "GENERATE_FAKE_RESULTS.$"

FAKE_THE_RESULTS = False

try:
    os.remove("saved_output.json")
except:
    pass

def loggy(s):
    msg = f"[DOCKERENTRYPOINT] {dt.now()}: {s}"
    print(msg)

class DockerEntryPoint:
    def __init__(self):
        loggy(f"DockerEntryPoint.__init__()")

    """
    def print_environment(self):
        print("##### FULL ENVIRONMENT (START) #####")
        for key in os.environ:
            print(f"\t'{key}' == '{os.environ[key]}'")
        print("##### FULL ENVIRONMENT (END) #####")
        print(f"just the tasktoken ({INCOMING_TOKEN_ENV_KEY}): '{os.environ.get(INCOMING_TOKEN_ENV_KEY)}'")
        print(f"just the scenarioid ({SCENARIO_ID_KEY}): '{os.environ.get(SCENARIO_ID_KEY)}'")
    """

    def attempt_task_conclusion(self, output_data):
        loggy(f"Attemping task conclusion iwth '{self.task_token}' / {output_data}...")
        try:
            client = boto3.client('stepfunctions')
            client.send_task_success(
                taskToken=self.task_token,
                output=json.dumps(output_data)
            )
        except Exception as e:
            loggy(f"ERROR DURING ATTEMPT_TASK_CONCLUSION: {e}")
        loggy("past  task conclusion!")

    # when used on AWS in a StepFunction/ECS flow, we get the input data from the environment.
    # Additionally, inn the StepFunction the scenario id actually has a $ in the name; I cannot figure out a way
    # to replicate that in local testing. So we search for both.
    def get_input_data_from_environment(self):
        global FAKE_THE_RESULTS
        self.task_token = os.environ.get(INCOMING_TOKEN_ENV_KEY)
        self.scenario_id = os.environ.get(SCENARIO_ID_KEY, None)
        if self.scenario_id is None:
            loggy(f"(unable to find scenario id using key '{SCENARIO_ID_KEY}'; attempting local $-less version. If you are running locally, this is not an error)")
            self.scenario_id = os.environ.get(SCENARIO_ID_KEY[0:-2])
        self.scenario_id = int(self.scenario_id)

        test_data_probe = os.environ.get(FAKE_KEY)
        if test_data_probe is not None and str(test_data_probe).lower() == "true":
            FAKE_THE_RESULTS = True

    def get_app_context(self):
        self.app = create_app()

        # tested this -- but didn't actually need it; in fact it's actually harmful (sets up
        # the listeners and all that, when all I need is like database connectivity)
        # print(f"Launching internal Flask app ({self.app})...")
        # self.app.run(port=6060)
        # print(f"launched!")
        """
        # testing - this works!
        with self.app.app_context():
                print(f"{dt.now()}: App context established!")
                s = ScenarioService.get(self.scenario_id)

                if s is None:
                    print(f"{dt.now()}: ERROR: unable to find scenario with id {self.scenario_id}; exiting.")
                    return
                else:
                    print(f"{dt.now()}: Loaded scenario {s.id} ({s.name}): {s.description}")
        """
        return self.app.app_context()

    # basically a ripoff of run_result_scenario in trim_frontend/scenarios/routes.py
    def run_model(self, scenario):
        global FAKE_THE_RESULTS
        print(f"RUN MODEL WITH {FAKE_THE_RESULTS=}")
        if FAKE_THE_RESULTS:
            with open("fake_path.txt", "w") as f:
                f.write("fake data\ni expect this to go onto S3")

            return {
                "outputMass": "fake_path.txt",
                "fakedData": {
                    "fake_scenario": scenario,
                    "title": "Seinfeld",
                    "description": "A show about nothing",
                    "cast": [
                        {"realname": "Jerry Seinfeld", "character": "Jerry Seinfeld"},
                        {"realname": "Julia Louis-Dreyfus", "character": "Elaine Benes"},
                        {"realname": "Jason Alexander", "character": "George Costanza"},
                        {"realname": "Michael Richards", "character": "Cosmo Kramer"}
                    ]
                }
            }
        else:
            loggy(f"Kick off run for scenario {scenario.id} ({scenario.name})...")
            try:
                json_n_avg, json_c_avg, output_file_n, output_file_c, output_file_tm = run_full_model(scenario)
                data_resp = {
                    "mass": json_n_avg,
                    "conc": json_c_avg,
                    # "mass": json.loads(json_n_avg),
                    # "conc": json.loads(json_c_avg),
                    "outputMass": output_file_n,
                    "outputConc": output_file_c,
                    "outputTM": output_file_tm
                }
            except Exception as e:
                loggy(e)
                data_resp = {"error": e}

        return data_resp

    def launch(self):
        global FAKE_THE_RESULTS
        loggy(f"DockerEntryPoint.launch(); back to real data")
        uuid = str(uuidlib.uuid1())
        storage_bucket_name = os.environ.get(STORAGE_BUCKET_NAME_KEY)
        # self.print_environment()
        loggy(f"uuid for this run is '{uuid}'; bucket is '{storage_bucket_name}'")

        self.get_input_data_from_environment()
        if self.task_token is None or self.scenario_id is None:
            loggy(f"ERROR: unable to find task token ({self.task_token}) or scenario id ({self.scenario_id}); exiting.")
            return

        loggy(f"Found task token '{self.task_token}' and scenario id '{self.scenario_id}' from environment")
        loggy(f"FAKE RESULTS AAA SET TO '{FAKE_THE_RESULTS}'")
        # FAKE_THE_RESULTS = True
        # loggy(f"FAKE RESULTS BBB SET TO '{FAKE_THE_RESULTS}'")

        model_output = None
        with self.get_app_context():
            loggy(f"App context established!")
            if not FAKE_THE_RESULTS:
                s = ScenarioService.get(self.scenario_id)
                readable_scenario = f"{s.id} ({s.name})" if s is not None else "INVALID!!!"
            else:
                s = { "id": 99, "name": "fake dummy scenario" }
                readable_scenario = f"{s['id']} ({s['name']})"

            if s is None:
                loggy(f"ERROR: unable to find scenario with id {self.scenario_id}; exiting.")
                return
            else:
                loggy(f"Loaded scenario {readable_scenario}; proceeding with model run...")
                model_output = self.run_model(s)
                loggy(f"Run complete!!!")

        # write the data to the bucket
        s3_client = boto3.client("s3")
        full_key = f"{uuid}/model_output.json"

        print(f"WRITE DATA TO '{full_key}'")
        try:
            s3_client.put_object(
                Body=json.dumps(model_output),
                Bucket=storage_bucket_name,
                Key=full_key
            )
        except Exception as e:
            loggy(f"ERROR WRITING DATA TO S3: {e}")

        for key_name in [ "outputMass", "outputConc", "outputTM" ]:
            output_file = model_output.get(key_name)
            print(f"output probe '{key_name}' is '{output_file}'")

            if output_file is not None and os.path.isfile(output_file) and os.path.exists(output_file):
                full_key = f"{uuid}/{key_name}.xlsx"
                print(f"upload it to '{full_key}'...")
                print(f"file S3 URL is https://{storage_bucket_name}.s3.amazonaws.com/{full_key}")

                try:
                    s3_client.put_object(
                        Body=open(output_file, "rb"),
                        Bucket=storage_bucket_name,
                        Key=full_key
                    )
                except Exception as e:
                    loggy(f"ERROR WRITING DATA TO S3: {e}")

                # The URL for output needs to be updated in the database for the frontend hrefs to work.
                # For local run they are not changed but for prod run, the created files in the model_run are
                # purged along with the docker container, so we need to have the s3 url instead.
                try:
                    with self.app.app_context():
                        loggy(f"App context established!")
                        if not FAKE_THE_RESULTS:
                            scen = ScenarioService.get(self.scenario_id)
                            if key_name == 'outputMass':
                                [v for v in scen.proc_status][0].result_file_nt = \
                                    f'https://{storage_bucket_name}.s3.amazonaws.com/{full_key}'
                            elif key_name == 'outputConc':
                                [v for v in scen.proc_status][0].result_file_conc = \
                                    f'https://{storage_bucket_name}.s3.amazonaws.com/{full_key}'
                            else:
                                [v for v in scen.proc_status][0].result_file_tm = \
                                    f'https://{storage_bucket_name}.s3.amazonaws.com/{full_key}'
                            ScenarioService.commit()
                except Exception as e:
                    loggy(f"ERROR STORING S3 URL in the DB: {e}")
            else:
                print(f"skip '{output_file}'; doesn't exist in this payload (maybe testing data...)")


        """
        if model_output is None:
            pass
        else:
            try:
                with open("saved_output.json", "w") as f:
                    json.dump(model_output, f)
            except:
                pass
        """

        self.attempt_task_conclusion({ "bucket": storage_bucket_name, "uuid": uuid })

        loggy(f"DONE!")

if __name__ == "__main__":
    dep = DockerEntryPoint()
    dep.launch()
