import os
import shutil
import tempfile
import time
from flask import request
from functools import wraps


MAX_CLEANUP_TRIES = 5


def with_tempdir(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        tempdir = None
        if not hasattr(request, 'tempdir'):
            tempdir = tempfile.mkdtemp()
            request.tempdir = tempdir

        def cleanup(tries=0):
            if not os.path.isdir(tempdir):
                return
            # Remove tempfile right away, if present
            try:
                shutil.rmtree(tempdir)
            except (
                PermissionError, FileNotFoundError, NotADirectoryError
            ):
                time.sleep(2)
                if tries < MAX_CLEANUP_TRIES:
                    cleanup(tries=(tries + 1))

        try:
            return f(*args, **kwargs)
        finally:
            cleanup()
    return decorated
