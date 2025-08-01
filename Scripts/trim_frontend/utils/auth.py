import os
from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password


def define_superusers(app, security):
    r = security.datastore.find_or_create_role('superuser')
    default_superuser = os.getenv('DEFAULT_SUPERUSER')
    if default_superuser is None:
        app.logger.warning('No default superuser specified')
    else:
        default_superuser_pwd = os.getenv('DEFAULT_SUPERUSER_PWD', '@dm1nUs3r')
        u = security.datastore.get_user(default_superuser)
        pwd = hash_password(default_superuser_pwd)
        if not u:
            security.datastore.create_user(
                email=default_superuser, password=pwd,
                confirmed_at=datetime.utcnow()
            )
            security.datastore.commit()
            u = security.datastore.get_user(default_superuser)
        # u.password = pwd
        security.datastore.add_role_to_user(u, r)
    security.datastore.commit()


def init_auth(app, db, bcrypt, security):
    bcrypt.init_app(app)
    from ..users.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    from ..users.forms import UserLoginForm, UserRegisterForm, \
        UserConfirmRegisterForm, UserForgotPasswordForm, \
        UserResetPasswordForm, UserChangePasswordForm

    # Flask-Security fails to bind this correctly when using init_app;
    # if they fix it, this assignment will become unecessary --
    # but for now, we need it.
    security._state = security.init_app(
        app,
        datastore=user_datastore,
        login_form=UserLoginForm,
        forgot_password_form=UserForgotPasswordForm,
        register_form=UserRegisterForm,
        confirm_register_form=UserConfirmRegisterForm,
        reset_password_form=UserResetPasswordForm,
        change_password_form=UserChangePasswordForm
    )

    from ..users.models import AnonUser
    app.login_manager.login_message_category = 'danger'
    app.login_manager.anonymous_user = AnonUser

    from trim_db.services import UserService

    # Add a request loader to enable Api-Key auth
    @app.login_manager.request_loader
    def load_request(request):
        # First check if an API key is present
        api_key = request.headers.get('api-key')  # AWS doesn't allow underscores!
        if api_key:
            u = UserService.from_key(value=api_key)
            if u is not None:
                return u
        return None
