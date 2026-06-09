import json, os, sys
from datetime import datetime as dt

# now that we run in a virtual environment within our Docker container,
# also need to point at this or qgis.core can't be imported...
sys.path.insert(0,"/usr/lib/python3/dist-packages")

import uuid as uuidlib

import boto3
from qgis.core import *

INCOMING_TOKEN_ENV_KEY = "TASK_TOKEN_ENV_VARIABLE"
STORAGE_BUCKET_NAME_KEY = "STORAGE_BUCKET_NAME"
SCENARIO_ID_KEY = "TRIM_SCENARIO_ID.$"

print(f"QUICK SHIM FOR GETFLOW, SETTING DB CREDS, CORRECT REORDERING!")

print(f"MAKE SECRET CLiENT...")
secrets_client = boto3.client('secretsmanager')
print(f"got if: {secrets_client}")

response = secrets_client.get_secret_value(
    SecretId='pytrim/database/credentials'
)

print(f"secrets response: {response}")
secret_data = json.loads(response['SecretString'])

engine = os.getenv('DB_ENGINE')
if engine == 'mysql':
    engine = 'mysql+pymysql'
elif engine == 'postgres':
    engine = 'postgresql+psycopg2'

# put stuff into environment variables...
os.environ["SQLALCHEMY_DATABASE_URI"] = (
    f"{engine}://"
    + f"{secret_data['username']}:{secret_data['password']}"
    + f"@{os.getenv('DB_HOSTNAME')}:{os.getenv('DB_PORT')}"
    + f"/{os.getenv('DB_NAME')}"
)

# verify what's in the environment
# print(f"ENVIRONMENT (start):")
# for key, value in os.environ.items():
#     print(f'{key}: {value}')
# print(f"ENVIRONMENT (end):")

from getflow import run_getflow_v13, run_getflow_v13_for_scenario_id
from trim_db import ScenarioService
from trim_frontend import create_app


print(f"QUICK SHIM END!")

try:
    os.remove("saved_output.json")
except:
    pass

def loggy(s):
    msg = f"[DOCKER_GETFLOW_ENTRYPOINT Aug2025 TueA] {dt.now()}: {s}"
    print(msg)

class DockerGetflowEntryPoint:
    def __init__(self):
        loggy(f"DockerGetflowEntryPoint.__init__()")

    def attempt_task_conclusion(self, output_data):
        loggy(f"Attemping task conclusion with '{self.task_token}' / {output_data}...")
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
        self.task_token = os.getenv(INCOMING_TOKEN_ENV_KEY)
        self.storage_bucket_name = os.getenv(STORAGE_BUCKET_NAME_KEY)
        self.scenario_id = int(os.getenv(SCENARIO_ID_KEY, -1))

        print(f"@@@@@@@@@@ ALL ENVIRONMENT START @@@@@@@@@@@@@@")
        for key, value in os.environ.items():
            print(f'[{key}]: [{value}]')
        print(f"@@@@@@@@@@ ALL ENVIRONMENT END @@@@@@@@@@@@@@")

    def get_app_context(self):
        self.app = create_app()
        return self.app.app_context()

    def launch_helper(self, parcels_or_scenario_id):
        # h/t https://gis.stackexchange.com/questions/348140/qgis-3-10-python-ide-application-path-not-initialized
        # see also https://docs.qgis.org/3.28/en/docs/pyqgis_developer_cookbook/index.html
        loggy("setup qgs application/path/initialization...")
        sys.path.append("/usr/share/qgis/python/plugins")
        qgs = QgsApplication([], False)
        QgsApplication.setPrefixPath("/usr/bin/qgis", True)
        QgsApplication.initQgis()

        loggy("initialize processing plugins...")
        import processing
        from processing.core.Processing import Processing
        Processing.initialize()

        loggy("initialize saga...")
        # this seems promising:
        # https://gis.stackexchange.com/a/456180
        # you need to unzip processing_saga_nextgen in your plugins dir...see Dockerfile
        from processing_saga_nextgen.saga_nextgen_plugin import SagaNextGenAlgorithmProvider
        provider = SagaNextGenAlgorithmProvider()
        provider.loadAlgorithms()
        QgsApplication.processingRegistry().addProvider(provider=provider)

        loggy("running getflow v13...")
        if type(parcels_or_scenario_id) is int:
            saved_outputs = run_getflow_v13_for_scenario_id(parcels_or_scenario_id)
        else:
            saved_outputs = run_getflow_v13(parcels)

        loggy(f"back from run_getflow_v13 ({saved_outputs})...")
        qgs.exitQgis()
        loggy("gis exited...")

        bucket, paths, presigned_urls = self.upload_results_to_s3(saved_outputs)

        return bucket, paths, presigned_urls

    def upload_results_to_s3(self, output_files):
        # write the data to the bucket
        s3_client = boto3.client("s3")
        """
        full_key = f"{self.uuid}/something.json"
        print(f"WRITE DATA TO '{full_key}'")
        try:
            s3_client.put_object(
                Body=json.dumps(model_output),
                Bucket=storage_bucket_name,
                Key=full_key
            )
        except Exception as e:
            loggy(f"ERROR WRITING DATA TO S3: {e}")
        """

        presigned_urls = []
        full_keys = []
        errored = False
        for output_file in output_files:
            key_name = output_file.split(os.path.sep)[-1]

            print(f"output probe '{key_name}' is '{output_file}'")

            if output_file is not None and os.path.isfile(output_file) and os.path.exists(output_file):
                full_key = f"{self.uuid}/{key_name}"
                print(f"upload it to '{full_key}'...")
                print(f"file S3 URL is https://{self.storage_bucket_name}.s3.amazonaws.com/{full_key}")

                try:
                    s3_client.put_object(
                        Body=open(output_file, "rb"),
                        Bucket=self.storage_bucket_name,
                        Key=full_key
                    )

                    presigned_url = self.create_presigned_url(s3_client, self.storage_bucket_name, full_key)

                    presigned_urls.append(presigned_url)
                    full_keys.append(full_key)

                    # return self.storage_bucket_name, full_key, presigned_url
                except Exception as e:
                    loggy(f"ERROR WRITING DATA TO S3: {e}")
                    errored = True
            else:
                print(f"skip '{output_file}'; not found somehow?")
                errored = True

        if errored:
            return None, None, None
        else:
            return self.storage_bucket_name, full_keys, presigned_urls
        
    def create_presigned_url(self, s3_client, bucket_name, object_name, expiration = 3600):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        :param expiration: Time in seconds for the presigned URL to remain valid
        :return: Presigned URL as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        try:
            response = s3_client.generate_presigned_url('get_object',
                                                        Params={'Bucket': bucket_name,
                                                                'Key': object_name},
                                                        ExpiresIn=expiration)
        except ClientError as e:
            logging.error(e)
            return None

        # The response contains the presigned URL
        return response

    def launch(self):
        loggy(f"DockerGetflowEntryPoint.launch()")
        self.uuid = str(uuidlib.uuid1())

        self.get_input_data_from_environment()

        loggy(f"uuid for this run is '{self.uuid}'; bucket is '{self.storage_bucket_name}'")
        """
        if self.task_token is None or self.something is None:
            loggy(f"ERROR: unable to find task token ({self.task_token}) or SOMETHING ({self.something}); exiting.")
            return
        """
        loggy(f"Found task token '{self.task_token}' and bucket '{self.storage_bucket_name}' from environment")

        loggy("app context attempt...")

        with self.get_app_context():
            scen = ScenarioService.get(self.scenario_id)
            print(f"loaded {scen} ({scen.name}) / ({scen.description}) [not really needed]...")

            # model_output = { "fake": "hardcoded_output" }
            # fake_parcels = { "x": "y" }
            # hardcode for now
            # fake_parcels = json.loads('{"E1": [[44.24230857894454, -85.36564449106953], [44.21761385490483, -85.39594865634041], [44.23446475981263, -85.42205322398412], [44.244984080277646, -85.40015747701385], [44.25070432459481, -85.40608220854818], [44.25529044063657, -85.38228207200879], [44.24230857894454, -85.36564449106953]], "E2": [[44.26507056695825, -85.33610064064906], [44.24230857894454, -85.36564449106953], [44.25529044063657, -85.38228207200879], [44.26980204643037, -85.37830428060558], [44.26507056695825, -85.33610064064906]], "E3": [[44.22647738643362, -85.33404253646208], [44.24230857894454, -85.36564449106953], [44.26507056695825, -85.33610064064906], [44.22647738643362, -85.33404253646208]], "LakeCadillac": [[44.23206535321081, -85.44781292630827], [44.24018602703797, -85.45013129952389], [44.24646032564297, -85.43673625431508], [44.25070432459481, -85.40608220854818], [44.244984080277646, -85.40015747701385], [44.23446475981263, -85.42205322398412], [44.23206535321081, -85.44781292630827]], "LakeMitchell": [[44.23970918183084, -85.45894643521314], [44.23464932547506, -85.45631362807308], [44.22892752001393, -85.48052774825459], [44.238525071310086, -85.48928604704837], [44.23631039070812, -85.51015140593478], [44.262881056386114, -85.49572597263389], [44.26878401863587, -85.48284612147161], [44.263803433303245, -85.47254224054217], [44.23970918183084, -85.45894643521314]], "N1": [[44.26696831920423, -85.43702373165462], [44.24646032564297, -85.43673625431508], [44.24018602703797, -85.45013129952389], [44.23970918183084, -85.45894643521314], [44.263803433303245, -85.47254224054217], [44.26878401863587, -85.48284612147161], [44.27417487841899, -85.4735100295159], [44.26696831920423, -85.43702373165462]], "N2": [[44.291009375300625, -85.40560961023537], [44.26696831920423, -85.43702373165462], [44.27417487841899, -85.4735100295159], [44.29193759780595, -85.48331523157111], [44.313482680048544, -85.49857586911367], [44.318920620853675, -85.42751294703508], [44.291009375300625, -85.40560961023537]], "NE1": [[44.26980204643037, -85.37830428060558], [44.25529044063657, -85.38228207200879], [44.25070432459481, -85.40608220854818], [44.24646032564297, -85.43673625431508], [44.26696831920423, -85.43702373165462], [44.291009375300625, -85.40560961023537], [44.26980204643037, -85.37830428060558]], "NE2": [[44.29875762171827, -85.38232693276689], [44.291009375300625, -85.40560961023537], [44.318920620853675, -85.42751294703508], [44.29875762171827, -85.38232693276689]], "NE3": [[44.26507056695825, -85.33610064064906], [44.26980204643037, -85.37830428060558], [44.291009375300625, -85.40560961023537], [44.29875762171827, -85.38232693276689], [44.26507056695825, -85.33610064064906]], "NW1": [[44.27417487841899, -85.4735100295159], [44.26878401863587, -85.48284612147161], [44.262881056386114, -85.49572597263389], [44.23631039070812, -85.51015140593478], [44.25439593613812, -85.56583916859093], [44.27992605076503, -85.5259089743607], [44.29193759780595, -85.48331523157111], [44.27417487841899, -85.4735100295159]], "NW2": [[44.29193759780595, -85.48331523157111], [44.27992605076503, -85.5259089743607], [44.25439593613812, -85.56583916859093], [44.27778718753971, -85.58841714514831], [44.313482680048544, -85.49857586911367], [44.29193759780595, -85.48331523157111]], "S1": [[44.23206535321081, -85.44781292630827], [44.23464932547506, -85.45631362807308], [44.23970918183084, -85.45894643521314], [44.24018602703797, -85.45013129952389], [44.23206535321081, -85.44781292630827]], "S2": [[44.21761385490483, -85.39594865634041], [44.21674520682198, -85.46420237645751], [44.23206535321081, -85.44781292630827], [44.23446475981263, -85.42205322398412], [44.21761385490483, -85.39594865634041]], "SE1": [[44.17957204740195, -85.45198221496595], [44.21674520682198, -85.46420237645751], [44.21761385490483, -85.39594865634041], [44.20226312542503, -85.35959166526649], [44.17957204740195, -85.45198221496595]], "SE2": [[44.22647738643362, -85.33404253646208], [44.20226312542503, -85.35959166526649], [44.21761385490483, -85.39594865634041], [44.24230857894454, -85.36564449106953], [44.22647738643362, -85.33404253646208]], "SW1": [[44.23464932547506, -85.45631362807308], [44.23206535321081, -85.44781292630827], [44.21674520682198, -85.46420237645751], [44.20943600317834, -85.51735250415958], [44.23631039070812, -85.51015140593478], [44.238525071310086, -85.48928604704837], [44.22892752001393, -85.48052774825459], [44.23464932547506, -85.45631362807308]], "SW2": [[44.20943600317834, -85.51735250415958], [44.21674520682198, -85.46420237645751], [44.17957204740195, -85.45198221496595], [44.18607795891237, -85.56167436349948], [44.222723194590145, -85.57903039347019], [44.20943600317834, -85.51735250415958]], "W1": [[44.23631039070812, -85.51015140593478], [44.20943600317834, -85.51735250415958], [44.222723194590145, -85.57903039347019], [44.25439593613812, -85.56583916859093], [44.23631039070812, -85.51015140593478]]}')

            # self.launch_helper(fake_parcels)
            bucket, paths, presigned_urls = self.launch_helper(self.scenario_id)

            self.attempt_task_conclusion({
                "run_uuid": self.uuid,
                "bucket": bucket,
                "paths": paths,
                "presigned_urls": presigned_urls
            })

        loggy(f"DONE!")

if __name__ == "__main__":
    ep = DockerGetflowEntryPoint()
    ep.launch()
