from flask_security.forms import LoginForm, \
    ForgotPasswordForm, RegisterForm, ConfirmRegisterForm, \
    PasswordConfirmFormMixin, ResetPasswordForm, \
    ChangePasswordForm, PasswordField, get_form_field_label
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Regexp
from ..utils.forms import OrderableForm


class UserInfoMixin:
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    company_name = StringField('Company', [DataRequired()])


class UserLoginForm(OrderableForm, LoginForm):
    field_order = (
        'email', 'password', '*'
    )


class UserForgotPasswordForm(ForgotPasswordForm):
    pass


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
