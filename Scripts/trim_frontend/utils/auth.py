import os
import json
import requests
import secrets
import boto3
from datetime import datetime
from urllib.parse import urlencode
from flask import request, redirect, url_for, abort, session
from flask_security import SQLAlchemyUserDatastore, current_user, login_user
from flask_security.utils import hash_password


def define_superusers(app, security):
    r = security.datastore.find_or_create_role('superuser')
    default_superuser = os.getenv('DEFAULT_SUPERUSER')
    if default_superuser is None:
        app.logger.warning('No default superuser specified')
    else:
        default_superuser_pwd = os.getenv('DEFAULT_SUPERUSER_PWD', '@dm1nUs3r')
        u = security.datastore.find_user(email=default_superuser)
        pwd = hash_password(default_superuser_pwd)
        if not u:
            security.datastore.create_user(
                email=default_superuser, password=pwd,
                confirmed_at=datetime.utcnow()
            )
            security.datastore.commit()
            u = security.datastore.find_user(email=default_superuser)
        # u.password = pwd
        security.datastore.add_role_to_user(u, r)
    security.datastore.commit()


class FlaskOauth:
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app, security=None):
        if hasattr(app, '_flask_oauth'):
            raise AssertionError('Cannot register FlaskOauth twice!')
        app._flask_oauth = self

        self._app = app
        if security:
            self._security = security

        self._oauth1_providers = {}
        self.register_providers(app.config.get('OAUTH_PROVIDERS'), oauth2=False)

        self._oauth2_providers = {}
        self.register_providers(app.config.get('OAUTH2_PROVIDERS'))

        @app.route('/oauth2/login/<provider_name>')
        def oauth2_login(provider_name):
            if not current_user.is_anonymous:
                return redirect(url_for('index'))

            provider = self._oauth2_providers.get(provider_name)
            if provider is None:
                abort(404)

            session['oauth2_state'] = secrets.token_urlsafe(16)

            query_args = {
                'client_id': provider['client_id'],
                'redirect_uri': self.get_callback_uri(provider),
                'response_type': 'code',
                'scope': ' '.join(provider['scopes']),
                'state': session['oauth2_state'],
            }

            return redirect(provider['authorize_url'] + '?' + urlencode(query_args))

    def get_client_secret(self, secret_id):
        if not secret_id:
            return None
        secrets_client = boto3.client('secretsmanager')
        response = secrets_client.get_secret_value(
            SecretId=secret_id
        )
        try:
            secret_data = json.loads(response['SecretString'])
        except:
            secret_data = response['SecretString']
        return secret_data['client_secret']

    def register_providers(self, providers, oauth2=True):
        if not providers:
            return
        if isinstance(providers, dict):
            providers = [{'name': p_name, **p} for p_name, p in providers.items()]
        for provider in providers:
            self.register_provider(provider, oauth2=oauth2)

    def get_callback_endpoint_name(self, provider):
        return f'oidc_callback_{provider["name"]}'

    def get_callback_uri(self, provider):
        return url_for(self.get_callback_endpoint_name(provider), _external=True)

    def register_provider(self, provider, oauth2=True):
        if not oauth2:
            return self._register_oauth1_provider(provider)
        else:
            self._register_oauth2_provider(provider)

    def _register_oauth1_provider(self, provider):
        raise NotImplementedError

    def _register_oauth2_provider(self, provider):
        self._oauth2_providers[provider['name']] = provider

        if 'client_secret' in provider:
            provider['client_secret'] = self.get_client_secret(secret_id=provider['client_secret'])

        @self._app.route(provider['redirect_endpoint'], endpoint=self.get_callback_endpoint_name(provider))
        def oidc_callback():
            if not current_user.is_anonymous:
                return redirect(url_for('index'))

            if request.args['state'] != session.get('oauth2_state'):
                abort(401)

            if 'code' not in request.args:
                abort(401)

            response = requests.post(
                provider['token_url'],
                data={
                    'client_id': provider['client_id'],
                    'client_secret': provider['client_secret'],
                    'code': request.args['code'],
                    'grant_type': 'authorization_code',
                    'redirect_uri': self.get_callback_uri(provider),
                },
                headers={'Accept': 'application/json'}
            )
            if response.status_code != 200:
                abort(401)
            oauth2_token = response.json().get('access_token')
            if not oauth2_token:
                abort(401)

            response = requests.get(provider['userinfo_url'], headers={
                'Authorization': 'Bearer ' + oauth2_token,
                'Accept': 'application/json',
            })
            if response.status_code != 200:
                abort(401)
            email = response.json()['email']

            user = self._security.datastore.find_user(email=email)
            if user is None:
                abort(401)

            login_user(user)
            return redirect(url_for('index'))


def init_auth(app, db, bcrypt, security):
    bcrypt.init_app(app)
    from ..users.models import User, Role
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)

    from ..users.forms import UserLoginForm, UserRegisterForm, \
        UserConfirmRegisterForm, UserForgotPasswordForm, \
        UserResetPasswordForm, UserChangePasswordForm

    # Flask-Security fails to bind _state correctly when using init_app;
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

    # Enable oauth login
    oauth = FlaskOauth()
    oauth.init_app(app, security)
