import logging
import os
from contextlib import contextmanager, redirect_stdout


class ConditionalFormatter(logging.Formatter):
    def format(self, record):
        if hasattr(record, 'no_formatting') and record.no_formatting:
            return record.getMessage()
        else:
            return logging.Formatter.format(self, record)


def make_logger(
    name, level=None,
    formatting='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    filepath=None
):
    if level is None:
        is_debug = os.getenv('FLASK_DEBUG')
        if is_debug:
            level = logging.DEBUG
        else:
            level = logging.INFO

    if isinstance(level, str):
        try:
            level = getattr(logging, level.upper())
        except AttributeError:
            level = logging.INFO

    logger = logging.Logger(name)

    f = ConditionalFormatter(formatting)

    h = logging.StreamHandler()
    h.setLevel(level)
    h.setFormatter(f)
    logger.addHandler(h)

    if filepath and os.path.isdir(os.path.dirname(filepath)):
        h = logging.FileHandler(filename=filepath, encoding='utf-8')
        h.setLevel(level)
        h.setFormatter(f)
        logger.addHandler(h)

    return logger


class LoggerWriter:
    def __init__(self, logger, level=logging.INFO):
        self.logger = logger
        self.level = level
        self.buffer = []

    def write(self, msg):
        self.buffer.append(msg)
        if msg.endswith('\n'):
            self.logger.log(self.level, ''.join(self.buffer).rstrip())
            self.buffer = []

    def flush(self):
        pass


@contextmanager
def stdout_to_logger(logger, level=logging.INFO):
    if isinstance(level, str):
        level = getattr(logging, level.upper(), logging.INFO)
    with redirect_stdout(LoggerWriter(logger, level)):
        yield
