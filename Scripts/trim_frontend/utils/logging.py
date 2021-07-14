import logging
import os


def make_logger(name):
    logger = logging.Logger(name)
    h = logging.StreamHandler()

    env = os.getenv('FLASK_ENV', 'production')
    if env == 'production':
        h.setLevel(logging.INFO)
    else:
        h.setLevel(logging.DEBUG)

    f = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'
    )
    h.setFormatter(f)

    logger.addHandler(h)

    return logger
