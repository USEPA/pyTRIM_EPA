import os, subprocess

WORKING_DIR = os.path.dirname(__file__)
BATCH_PATH = os.path.join(WORKING_DIR, "startup_RUSLE_QGIS.bat")

subprocess.run(f"{BATCH_PATH} start")
