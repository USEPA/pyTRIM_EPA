import requests


class ApiMeta(type):
    _headers = {
        'Authorization': None,
        'Content-Type': 'application/json'
    }
    _session = None

    @property
    def root(cls):
        return 'http://csip.engr.colostate.edu:8088/csip-misc/d/r2climate/3.0'

    @property
    def headers(cls):
        return cls._headers

    @property
    def session(cls):
        if cls._session is None:
            cls._session = requests.Session()
        cls._session.headers.update(cls.headers)
        return cls._session


class UsleClimateApi(metaclass=ApiMeta):
    @classmethod
    def get_r_value(cls, latitude, longitude):
        data = {
            'parameter': [
                {
                    'name': "latitude",
                    'value': latitude
                },
                {
                    'name': "longitude",
                    'value': longitude
                }
            ]
        }

        resp = requests.post(cls.root, json=data, headers=cls._headers)
        data = resp.json()
        results = data["result"][1]["value"]["Obj"]["Flt"][0]
        return results['Data']