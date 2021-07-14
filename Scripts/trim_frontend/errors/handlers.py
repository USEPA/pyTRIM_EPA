import traceback
from flask import Blueprint, render_template
from jinja2.exceptions import TemplateNotFound
from werkzeug.exceptions import NotFound
from werkzeug.routing import BuildError
from ..utils.logging import make_logger

errors = Blueprint('errors', __name__)

custom_errors = {
    404: "The page you requested does not exist.",
    403: ("You don't have permission to do that; "
          "please check your account and try again."),
    400: ("The browser (or proxy) sent a request "
          "that our server could not understand."),
    500: "Something went wrong. Please try again."
}


@errors.app_errorhandler(Exception)
def err_generic(error):
    err_type = error.__class__.__name__
    if (
        isinstance(error, BuildError) or
        isinstance(error, TemplateNotFound)
    ):
        raise error

    if not hasattr(error, 'code'):
        setattr(
            error, 'description',
            " ".join([str(arg) for arg in error.args])
        )
        setattr(error, 'code', 500)
    elif error.code in custom_errors:
        error.description = custom_errors.get(error.code)

    if not hasattr(error, 'name'):
        setattr(error, 'name', err_type)

    if not isinstance(error, NotFound):
        logger = make_logger('app_error')
        logger.error(f'{error}\n{traceback.format_exc()}')

    return render_template('errors/generic.html', e=error), error.code
