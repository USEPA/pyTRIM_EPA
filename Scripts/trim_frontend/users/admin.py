from flask_security.utils import hash_password
from wtforms.widgets import PasswordInput
from trim_frontend import db
from .models import User, Role
from ..utils.admin_views import AdminModelView, AdminScenarioView


class UserAdminView(AdminModelView):
    def create_model(self, form):
        if form.password.data:
            form.password.process_data(hash_password(form.password.data))
        
        return super().create_model(form)
    
    def update_model(self, form, model):
        if not form.password.data:
            form.password.process_data(model.password)

        if form.password.data != model.password:
            form.password.process_data(hash_password(form.password.data))

        return super().update_model(form, model)

    def on_form_prefill(self, form, id):
        form.password.widget = PasswordInput()
        form.password.process_data('')


users_category = 'Authentication'

admin_views = [
    UserAdminView(
        User, db.session, name='Users', category=users_category,
        delete=False,
        column_list=['email', 'roles', 'active', 'last_login_at'],
        column_default_sort=('email', False),
        column_filters=['email', 'roles.name', 'active'],
        form_columns=[
            'email', 'password', 'roles', 'active', 'confirmed_at'
        ]
    ),
    AdminModelView(
        Role, db.session, name='Roles', category=users_category,
        delete=False
    ),
    AdminScenarioView(
        name="Scenarios", endpoint='scenarios'
    )
]
