import json, os, sys
from datetime import datetime as dt

import boto3
from qgis.core import *

from getflow import run_getflow_v7

INCOMING_TOKEN_ENV_KEY = "TASK_TOKEN_ENV_VARIABLE"

print(f"QUICK SHIM FOR GETFLOW!")


try:
    os.remove("saved_output.json")
except:
    pass

def loggy(s):
    msg = f"[DOCKER_GETFLOW_ENTRYPOINT] {dt.now()}: {s}"
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
        self.task_token = os.environ.get(INCOMING_TOKEN_ENV_KEY)
        self.something = os.environ.get("SOME_ENV_VARIABLE", None)


    def launch_helper(self, parcels):
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

        loggy("running getflow...")
        run_getflow_v7(parcels)
        loggy("back from run_getflow_v7...")
        qgs.exitQgis()
        loggy("gis exited...")

    def launch(self):
        loggy(f"DockerGetflowEntryPoint.launch()")
        # uuid = str(uuidlib.uuid1())
        # storage_bucket_name = os.environ.get(STORAGE_BUCKET_NAME_KEY)
        # self.print_environment()
        # loggy(f"uuid for this run is '{uuid}'; bucket is '{storage_bucket_name}'")

        self.get_input_data_from_environment()
        """
        if self.task_token is None or self.something is None:
            loggy(f"ERROR: unable to find task token ({self.task_token}) or SOMETHING ({self.something}); exiting.")
            return
        """
        loggy(f"Found task token '{self.task_token}' and SOMETHING '{self.something}' from environment")

        # model_output = { "fake": "hardcoded_output" }
        # fake_parcels = { "x": "y" }
        # hardcode for now
        fake_parcels = json.loads('{"E1": [[44.24230857894454, -85.36564449106953], [44.21761385490483, -85.39594865634041], [44.23446475981263, -85.42205322398412], [44.244984080277646, -85.40015747701385], [44.25070432459481, -85.40608220854818], [44.25529044063657, -85.38228207200879], [44.24230857894454, -85.36564449106953]], "E2": [[44.26507056695825, -85.33610064064906], [44.24230857894454, -85.36564449106953], [44.25529044063657, -85.38228207200879], [44.26980204643037, -85.37830428060558], [44.26507056695825, -85.33610064064906]], "E3": [[44.22647738643362, -85.33404253646208], [44.24230857894454, -85.36564449106953], [44.26507056695825, -85.33610064064906], [44.22647738643362, -85.33404253646208]], "LakeCadillac": [[44.23206535321081, -85.44781292630827], [44.24018602703797, -85.45013129952389], [44.24646032564297, -85.43673625431508], [44.25070432459481, -85.40608220854818], [44.244984080277646, -85.40015747701385], [44.23446475981263, -85.42205322398412], [44.23206535321081, -85.44781292630827]], "LakeMitchell": [[44.23970918183084, -85.45894643521314], [44.23464932547506, -85.45631362807308], [44.22892752001393, -85.48052774825459], [44.238525071310086, -85.48928604704837], [44.23631039070812, -85.51015140593478], [44.262881056386114, -85.49572597263389], [44.26878401863587, -85.48284612147161], [44.263803433303245, -85.47254224054217], [44.23970918183084, -85.45894643521314]], "N1": [[44.26696831920423, -85.43702373165462], [44.24646032564297, -85.43673625431508], [44.24018602703797, -85.45013129952389], [44.23970918183084, -85.45894643521314], [44.263803433303245, -85.47254224054217], [44.26878401863587, -85.48284612147161], [44.27417487841899, -85.4735100295159], [44.26696831920423, -85.43702373165462]], "N2": [[44.291009375300625, -85.40560961023537], [44.26696831920423, -85.43702373165462], [44.27417487841899, -85.4735100295159], [44.29193759780595, -85.48331523157111], [44.313482680048544, -85.49857586911367], [44.318920620853675, -85.42751294703508], [44.291009375300625, -85.40560961023537]], "NE1": [[44.26980204643037, -85.37830428060558], [44.25529044063657, -85.38228207200879], [44.25070432459481, -85.40608220854818], [44.24646032564297, -85.43673625431508], [44.26696831920423, -85.43702373165462], [44.291009375300625, -85.40560961023537], [44.26980204643037, -85.37830428060558]], "NE2": [[44.29875762171827, -85.38232693276689], [44.291009375300625, -85.40560961023537], [44.318920620853675, -85.42751294703508], [44.29875762171827, -85.38232693276689]], "NE3": [[44.26507056695825, -85.33610064064906], [44.26980204643037, -85.37830428060558], [44.291009375300625, -85.40560961023537], [44.29875762171827, -85.38232693276689], [44.26507056695825, -85.33610064064906]], "NW1": [[44.27417487841899, -85.4735100295159], [44.26878401863587, -85.48284612147161], [44.262881056386114, -85.49572597263389], [44.23631039070812, -85.51015140593478], [44.25439593613812, -85.56583916859093], [44.27992605076503, -85.5259089743607], [44.29193759780595, -85.48331523157111], [44.27417487841899, -85.4735100295159]], "NW2": [[44.29193759780595, -85.48331523157111], [44.27992605076503, -85.5259089743607], [44.25439593613812, -85.56583916859093], [44.27778718753971, -85.58841714514831], [44.313482680048544, -85.49857586911367], [44.29193759780595, -85.48331523157111]], "S1": [[44.23206535321081, -85.44781292630827], [44.23464932547506, -85.45631362807308], [44.23970918183084, -85.45894643521314], [44.24018602703797, -85.45013129952389], [44.23206535321081, -85.44781292630827]], "S2": [[44.21761385490483, -85.39594865634041], [44.21674520682198, -85.46420237645751], [44.23206535321081, -85.44781292630827], [44.23446475981263, -85.42205322398412], [44.21761385490483, -85.39594865634041]], "SE1": [[44.17957204740195, -85.45198221496595], [44.21674520682198, -85.46420237645751], [44.21761385490483, -85.39594865634041], [44.20226312542503, -85.35959166526649], [44.17957204740195, -85.45198221496595]], "SE2": [[44.22647738643362, -85.33404253646208], [44.20226312542503, -85.35959166526649], [44.21761385490483, -85.39594865634041], [44.24230857894454, -85.36564449106953], [44.22647738643362, -85.33404253646208]], "SW1": [[44.23464932547506, -85.45631362807308], [44.23206535321081, -85.44781292630827], [44.21674520682198, -85.46420237645751], [44.20943600317834, -85.51735250415958], [44.23631039070812, -85.51015140593478], [44.238525071310086, -85.48928604704837], [44.22892752001393, -85.48052774825459], [44.23464932547506, -85.45631362807308]], "SW2": [[44.20943600317834, -85.51735250415958], [44.21674520682198, -85.46420237645751], [44.17957204740195, -85.45198221496595], [44.18607795891237, -85.56167436349948], [44.222723194590145, -85.57903039347019], [44.20943600317834, -85.51735250415958]], "W1": [[44.23631039070812, -85.51015140593478], [44.20943600317834, -85.51735250415958], [44.222723194590145, -85.57903039347019], [44.25439593613812, -85.56583916859093], [44.23631039070812, -85.51015140593478]]}')

        self.launch_helper(fake_parcels)

        self.attempt_task_conclusion({ "fakeoutput": "yo", "hello": "tibs" })

        loggy(f"DONE!")

if __name__ == "__main__":
    ep = DockerGetflowEntryPoint()
    ep.launch()
