import os, sys, json, traceback
from pathlib import Path

scripts_dir = Path(__file__).parent.parent.resolve()
assert scripts_dir.name == "Scripts"
sys.path.append(str(scripts_dir))

try:
    try:
        from pipenv.vendor.dotenv import load_dotenv
    except:
        from dotenv import load_dotenv

    load_dotenv(Path(scripts_dir, ".env"))
except Exception as e:
    print(e)

os.environ["TEST_DB_SERVERLESS"] = "True"

from alembic import op
import sqlalchemy as sa
import pandas as pd
import numpy as np

from trim_db.schema import *
from trim_db.services import *
from trim_db.porting import *

# from trim_db.local import *  # implement_users_roles()

# this is needed to avoid sometimes calling implement_users_roles()
from trim_frontend.utils.logging import make_logger

logger = make_logger("headless")
