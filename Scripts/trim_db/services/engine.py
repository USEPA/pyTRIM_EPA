import json
import os
import sqlalchemy as sa
from ..schema.utils.base import Model

__all__ = [
    'DataBase', 'get_env_db_uri'
]


class DataBase:
    def __init__(self, uri, model_base=Model):
        self.uri = uri
        self._create_engine()

        if model_base:
            self._init_model_base(model_base)

    def _create_engine(self):
        self.engine = sa.create_engine(
            self.uri  #, connect_args={'check_same_thread': False}
        )
        print("Created new database connection")
        self._session = None

    def _make_session(self):
        s = sa.orm.Session(bind=self.engine)
        return s

    def _init_model_base(self, model_base):
        class _QueryProperty:
            def __init__(self, db):
                self.db = db

            def __get__(self, obj, cls):
                return self.db.session.query(cls)
        model_base.query = _QueryProperty(self)
        self.Model = model_base

    @property
    def session(self):
        if self._session is None:
            self._session = self._make_session()
        return self._session


def get_env_db_uri():
    if 'SQLALCHEMY_DATABASE_URI' in os.environ:
        return os.environ['SQLALCHEMY_DATABASE_URI']

    elif 'DB_ENGINE' in os.environ:
        engine = os.environ['DB_ENGINE']
        db_host = os.environ['DB_HOSTNAME']
        db_port = os.environ['DB_PORT']
        db_name = os.environ['DB_NAME']

        if 'DB_PASSWORD' in os.environ:
            uname = os.environ['DB_USERNAME']
            pword = os.environ['DB_PASSWORD']
        else:
            try:
                import boto3
                sm_client = boto3.client('secretsmanager')
                creds = json.loads(sm_client.get_secret_value(
                    SecretId='pytrim/database/credentials'
                ))
                uname = creds['username']
                pword = creds['password']
            except ModuleNotFoundError:
                raise RuntimeError('Unable to Load AWS Credentials; boto3 not found')

        print(f'-- Connecting to {engine.upper()} DB')
        if engine == 'mysql':
            engine = 'mysql+pymysql'
        db_uri = f'{engine}://{uname}:{pword}@{db_host}:{db_port}/{db_name}'

    else:
        print('-- Connecting to local SQLite db')
        db_uri = (
            'sqlite:///'
            + f'{os.path.dirname(os.path.abspath(__file__))}'
            + '/../../'
            + os.getenv('SQLITE_DB_NAME', 'database.db')
        )

    return db_uri
