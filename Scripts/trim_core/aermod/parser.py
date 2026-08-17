import pandas as pd
import re
from decimal import Decimal
from typing import IO


__all__ = ['AermodReader', 'read_aermod']

COLUMN_TYPES = {
    'X': float,
    'Y': float,
    'AVERAGE CONC': Decimal,  # floats are sometimes imprecise
    'DRY DEPO': Decimal,  # floats are sometimes imprecise
    'WET DEPO': Decimal,  # floats are sometimes imprecise
    'ZELEV': float,
    'ZHILL': float,
    'ZFLAG': float,
    'NUM HRS': float
}

COLUMN_SPACER = re.compile(r'[ ]{2,}')


class AermodReader:
    def __init__(self, ioWrapper: IO):
        self._raw_data = ioWrapper.readlines()
        if isinstance(self._raw_data[0], bytes):
            self._raw_data = [ln.decode('utf-8') for ln in self._raw_data]
        self._data = AermodReader.parse(self._raw_data)

    @classmethod
    def parse(cls, raw_data: list[str]) -> list[dict]:
        cols = None
        parsed = []
        for line in raw_data:
            line = line.strip()
            if not line:
                continue
            if line.startswith('*'):  # This is a comment
                if cols is None:  # Is it the column headers?
                    vals = COLUMN_SPACER.split(line)
                    normed = [x.upper() for x in vals[1:]]
                    if cls._is_valid_column_headers(normed):
                        cols = normed
                continue
            elif cols is None:  # Data before columns?
                raise ValueError('No Column Headers Detected')
            else:
                vals = line.split()
                entry = dict(zip(cols, vals))
                if not cls._is_valid_entry(entry):
                    continue
                parsed.append(cls._fix_types(entry))
        return parsed

    @classmethod
    def _is_valid_column_headers(cls, cols: list) -> bool:
        return ('X' in cols) and ('Y' in cols)

    @classmethod
    def _is_valid_entry(cls, entry: dict) -> bool:
        return (entry['X'] and entry['Y'])

    @classmethod
    def _fix_types(cls, entry: dict) -> dict:
        fixed = {}
        for k, v in entry.items():
            if k in COLUMN_TYPES:
                fixed[k] = COLUMN_TYPES[k](v)
            else:
                fixed[k] = v
        return fixed

    def __iter__(self):
        return iter(self._data)

    def as_dataframe(self):
        df = pd.DataFrame(self._data)
        # Dataframe math doesn't like Decimals, so we need to convert back to floats, sadly
        for k, v in COLUMN_TYPES.items():
            if k in df.columns.values and issubclass(v, Decimal):
                df[k] = df[k].astype(float)
        return df


def read_aermod(filepath, encoding='utf-8'):
    """A convenience generator that wraps AermodReader and yields entries"""
    with open(filepath, 'r', encoding=encoding) as f:
        reader = AermodReader(f)
        for entry in reader:
            yield entry
