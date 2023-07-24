import os


app_folder = os.path.abspath(os.path.dirname(__file__))
root = os.path.dirname(app_folder)
has_mail = os.getenv('MAIL_USERNAME') is not None


class AppConfig:
    # Template config
    TEMPLATES_AUTO_RELOAD = True

    # Static Assets config
    AUTO_BUILD = False

    # DB config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

    # Migrations config
    MIGRATIONS_PATH = os.path.join(root, 'trim_db', 'migrations')

    # Security config
    SECURITY_PASSWORD_HASH = 'bcrypt'
    SECURITY_REGISTERABLE = True
    SECURITY_TRACKABLE = True
    SECURITY_CONFIRMABLE = has_mail
    SECURITY_CHANGEABLE = has_mail
    SECURITY_RECOVERABLE = has_mail

    # Custom message config
    bad_login = ("The username or password is invalid", 'error')
    SECURITY_MSG_USER_DOES_NOT_EXIST = bad_login
    SECURITY_MSG_INVALID_PASSWORD = bad_login

    # Email config
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.getenv(
        'MAIL_DEFAULT_SENDER', MAIL_USERNAME
    )
    MAIL_RESPONSE_ADDRESS = os.getenv(
        'MAIL_RESPONSE_ADDRESS', MAIL_DEFAULT_SENDER
    )

    # You need to EXPLICITLY set this to avoid a bug
    SECURITY_EMAIL_SENDER = MAIL_DEFAULT_SENDER

    # BOTO config
    BOTO_AWS_KEY = ''
    BOTO_AWS_SECRET = ''
    BOTO_S3_BUCKET = ''
    BOTO_AWS_REGION = 'us-east-1'


class ProdConfig(AppConfig):
    SECRET_KEY = os.getenv('SECRET_KEY', '')
    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', '')


class DevConfig(AppConfig):
    SECRET_KEY = 'dcf917c34aec178987494a853bffa479'
    SECURITY_PASSWORD_SALT = ''
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{root}/database.db'
    SQLALCHEMY_ECHO = False


class TestConfig(DevConfig):
    TESTING = True
    LOGIN_DISABLED = False
    WTF_CSRF_ENABLED = False
    BCRYPT_LOG_ROUNDS = 4
    MAIL_SUPPRESS_SEND = True
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{app_folder}/test.db'
    # SQLALCHEMY_DATABASE_URI = f'sqlite:///{root}/database.db'

    # Security config
    SECURITY_CONFIRMABLE = False

    # Static Assets
    AUTO_BUILD = True
    CACHE = False


def init_config(app, testing=False):
    env = os.getenv('FLASK_ENV', 'production')
    # app.logger.info(f'************ Flask_env is {env}, Root is {root} and App_folder is {app_folder} ***************')
    if env == 'development':
        if testing:
            app.config.from_object(TestConfig)
        else:
            app.config.from_object(DevConfig)
    else:
        app.config.from_object(ProdConfig)
