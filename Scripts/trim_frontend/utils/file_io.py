import os
import pandas as pd
import tempfile


TRY_ENCODINGS = [
    'utf-8-sig',
    'cp1252',  # ANSI
    'latin-1',
    'ascii'
]


def csv_to_df(file, encoding='utf-8-sig', dtype=None):
    def read_csv(file, encoding, dtype=None):
        try:
            return pd.read_csv(file, encoding=encoding, dtype=dtype)
        except UnicodeDecodeError as e:
            for enc in TRY_ENCODINGS:
                try:
                    return pd.read_csv(file, encoding=enc, dtype=dtype)
                except UnicodeDecodeError:
                    pass
            raise e

    if hasattr(file, 'save'):
        with tempfile.TemporaryDirectory() as tmpdir:
            fpath = os.path.join(tmpdir, file.filename)
            file.save(fpath)
            return read_csv(fpath, encoding, dtype=dtype)

    return read_csv(file, encoding, dtype=dtype)
