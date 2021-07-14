from flask import Flask, after_this_request
from flask_wtf.csrf import CSRFProtect
from functools import wraps
from .blueprints import CrudBlueprint  # noqa
from .responses import ApiResult, ApiException, ApiFileResult  # noqa
from .utils.tempfiles import with_tempdir  # noqa
from .utils.validation import get_jwt  # noqa


class FlaskApi:
    serializer = None
    csrf_protect = True

    def __init__(self, app=None, *args, **kwargs):
        self._setup_csrf()

        if app:
            self.init_app(app, **kwargs)
        else:
            self._set_options(**kwargs)

    def _setup_csrf(self):
        self._csrf = CSRFProtect()
        self.csrf_exempt = self._csrf.exempt

    def _set_options(self, **options):
        self.serializer = options.pop(
            'default_serializer', self.serializer
        )

        self.csrf_protect = options.pop(
            'csrf_protect', self.csrf_protect
        )

    def init_app(self, app, **kwargs):
        self._app = app
        self._set_options(**kwargs)

        if self.csrf_protect:
            self._csrf.init_app(self._app)

        def make_response(rv):
            if isinstance(rv, ApiResult):
                return rv.to_response(serializer=self.serializer)
            return Flask.make_response(app, rv)

        self._app.make_response = make_response

        @self._app.errorhandler(ApiException)
        def err_api(error):
            return error.to_response(serializer=self.serializer)

    def use_api_errors(self, blueprint):
        @blueprint.errorhandler(Exception)
        def err_api(error):
            if isinstance(error, ApiException):
                return error.to_response(serializer=self.serializer)

            code = getattr(error, 'code', 500)
            message = str(error)

            api_err = ApiException(message, status=code)
            return api_err.to_response(serializer=self.serializer)

    def validate(self, validator, **options):
        def decorated(f):
            @wraps(f)
            def validated(*args, **kwargs):
                validator(**options)
                return f(*args, **kwargs)
            return self.csrf_exempt(validated)
        return decorated

    def encrypt_response(self, service, **options):
        def decorated(f):
            @wraps(f)
            def encrypted(*args, **kwargs):
                @after_this_request
                def encrypt_response(response):
                    service(response, **options)
                    return response
                return f(*args, **kwargs)
            return encrypted
        return decorated
