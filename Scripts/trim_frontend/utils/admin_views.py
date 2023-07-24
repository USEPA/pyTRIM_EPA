from flask import abort
from flask_admin import AdminIndexView, BaseView, expose
from flask_admin.base import _wrap_view
from flask_admin.contrib.fileadmin.s3 import S3FileAdmin
from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from trim_db.schema.scenarios.models import *
from trim_frontend.users.models import *
from trim_frontend.scenarios.forms import ScenarioDefinitionForm
from .class_utils import add_method


class AuthMixin:
    hide_if_inaccessible = False
    required_roles = None

    def is_accessible(self):
        if self.required_roles:
            return (current_user.is_authenticated and
                    current_user.has_any_role(self.required_roles))
        else:
            return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        if self.hide_if_inaccessible:
            return abort(404)
        else:
            return abort(403)


class AdminAuthMixin(AuthMixin):
    edit_modal = True
    required_roles = 'superuser'
    hide_if_inaccessible = True


class RestrictableMixin:
    def __init__(
        self, *args,
        create=True, edit=True, delete=True,
        **kwargs
    ):
        self.can_create = create
        self.can_mkdir = create
        self.can_upload = create
        self.can_edit = edit
        self.can_rename = edit
        self.can_delete = delete
        self.can_delete_dirs = delete

        for k in kwargs.copy():
            if hasattr(self, k):
                setattr(self, k, kwargs.pop(k))

        super().__init__(*args, **kwargs)


class AuthModelView(RestrictableMixin, AuthMixin, ModelView):
    pass


class AuthS3FileView(RestrictableMixin, AuthMixin, S3FileAdmin):
    pass


class AuthBaseView(AuthMixin, BaseView):
    pass


class AuthAdminIndexView(AdminAuthMixin, AdminIndexView):
    pass


class AdminModelView(AdminAuthMixin, AuthModelView):
    can_view_details = True


class AdminS3FileView(AdminAuthMixin, AuthS3FileView):
    pass


class AdminBaseView(AdminAuthMixin, AuthBaseView):
    @expose('/')
    def index(self):
        return abort(501)

    def __init__(self, *args, **kwargs):
        route_info = kwargs.pop('routes', {})

        for info in route_info:
            route = info.get('route', None)
            template = info.get('template', None)
            methods = info.get('methods', ('GET',))

            fname = route.rsplit('.', 1)[0]
            fname = fname.rsplit('/', 1)
            fname = fname[1] if len(fname) > 1 else fname[0]
            fname = 'index' if not fname.strip() else fname

            exposed = expose(route, methods)(
                lambda x, t=template: x.render(t)
            )
            add_method(self, name=fname, instance_method=True)(
                _wrap_view(exposed)
            )

            if fname != 'index':
                self._urls.append((route, fname, methods))

        super().__init__(*args, **kwargs)


class AdminScenarioView(AdminBaseView):
    @expose('/')
    def index(self):
        all_users = User.query.all()
        all_scenarios = Scenario.query.all()
        scenario_form = ScenarioDefinitionForm()
        return self.render('./admin/copy_scenario.html', scenario_form=scenario_form, scenarios=all_scenarios, users=all_users)


def init_admin_views(app, admin):
    admin.init_app(app, index_view=AuthAdminIndexView())

    # First import User models & views; many things depend on them
    from ..users.admin import admin_views
    for view in admin_views:
        admin.add_view(view)

    # add_s3_admin_view(app, admin)


def add_s3_admin_view(app, admin):
    try:
        key_id = app.config.get('BOTO_AWS_KEY')
        secret_key = app.config.get('BOTO_AWS_SECRET')
        bucket = app.config.get('BOTO_S3_BUCKET')
        region = app.config.get('BOTO_AWS_REGION', 'us-east-1')

        admin.add_view(AdminS3FileView(
            bucket, region, key_id, secret_key,
            name='S3 Storage',
            create=False, edit=False, delete=False
        ))
    except Exception as e:
        app.logger.warning(
            f'Unable to initialize S3 File Admin view: {e}'
        )
