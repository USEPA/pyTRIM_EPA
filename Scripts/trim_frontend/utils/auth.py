from flask_security import SQLAlchemyUserDatastore
from flask_security.utils import hash_password


def define_superusers(app, security):
    superusers = [
        'josiah.mccoy@icf.com',
    ]
    r = security.datastore.find_or_create_role('superuser')
    for name in superusers:
        u = security.datastore.get_user(name)
        if not u:
            security.datastore.create_user(
                email=name,
                password=hash_password('@dm1nUs3r')
            )
            u = security.datastore.get_user(name)
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
