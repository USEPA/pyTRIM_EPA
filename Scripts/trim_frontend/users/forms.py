from flask_security.forms import LoginForm, \
    ForgotPasswordForm, RegisterForm, ConfirmRegisterForm, \
    PasswordConfirmFormMixin, ResetPasswordForm, \
    ChangePasswordForm, PasswordField, get_form_field_label
from flask_security.utils import hash_password
from flask_security.confirmable import requires_confirmation, confirm_user
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from Scripts.trim_frontend import security, db
from ..utils.forms import OrderableForm


class UserInfoMixin:
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    company_name = StringField('Company', [DataRequired()])


def update_old_user_model(user, password=None):
    # If we ever get all users updated in the db,
    # We can remove this custom validation.

    # Make sure the user is in our session
    db.session.add(db.session.merge(user))
    if user and user.password.startswith('pbkdf2:sha256:'):
        # Because we used to hash passwords ourselves,
        # old users will need their password hash updated!
        if password and check_password_hash(user.password, password):
            print(
                "Warning: Old password hash detected. "
                "Updating stored hash."
            )
            user.password = hash_password(password)

        # Also auto-confirm old users
        if (requires_confirmation(user)):
            print(
                "Warning: Old user needs confirmation. "
                "Confirming by default."
            )
            confirm_user(user)
        db.session.commit()


class UserLoginForm(LoginForm):
    def validate(self):
        user = security.datastore.get_user(self.email.data)
        update_old_user_model(user, self.password.data)
        return super().validate()


class UserForgotPasswordForm(ForgotPasswordForm):
    def validate(self):
        user = security.datastore.get_user(self.email.data)
        update_old_user_model(user)
        return super().validate()


class PasswordRegex(Regexp):
    regex = (
        r"^(?=.*[a-z])(?=.*[A-Z])"
        r"(?=.*[0-9])(?=.*[!@#\$%\^&\*])"
        r"(?=.{8,})"
    )
    message = (
        "Password must contain at least 1 uppercase letter, "
        "1 lowercase letter, 1 digit, and 1 symbol (!@#$%^&*)"
    )

    def __init__(self):
        super().__init__(self.regex, message=self.message)


strong_pwd_validators = [
    DataRequired(message="Password not provided"),
    Length(
        min=8, max=128,
        message=("Password must be at least 8 characters")
    ),
    PasswordRegex()
]


class UserRegisterForm(OrderableForm, UserInfoMixin,
                       RegisterForm):
    field_order = (
        'first_name', 'last_name', 'email', 'company_name',
        'password', 'password_confirm', '*'
    )
    password = PasswordField(
        get_form_field_label('password'),
        validators=strong_pwd_validators
    )


# When using Flask-Security SECURITY_CONFIRMABLE = True,
# Flask uses a different register form,
# so we need to extend that one, too.
class UserConfirmRegisterForm(
    OrderableForm, UserInfoMixin, ConfirmRegisterForm,
    PasswordConfirmFormMixin
):
    field_order = (
        'first_name', 'last_name', 'email', 'company_name',
        'password', 'password_confirm', '*'
    )
    password = PasswordField(
        get_form_field_label('password'),
        validators=strong_pwd_validators
    )


class UserResetPasswordForm(OrderableForm, ResetPasswordForm):
    field_order = ('password', 'password_confirm', '*')
    password = PasswordField(
        get_form_field_label('password'),
        validators=strong_pwd_validators
    )


class UserChangePasswordForm(OrderableForm, ChangePasswordForm):
    field_order = (
        'password', 'new_password', 'new_password_confirm', '*'
    )
    new_password = PasswordField(
        get_form_field_label('new_password'),
        validators=strong_pwd_validators
    )


class EditUserForm(UserInfoMixin, FlaskForm):
    title = "Edit Personal Information"
    submit = SubmitField('Save')
