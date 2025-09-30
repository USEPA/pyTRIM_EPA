import sqlalchemy as sa
from sqlalchemy.ext.declarative import declared_attr
from ..utils.base import Model
from ..utils.mixins import ActiveFlagMixin
from ..utils.permissions import PermissionsEnum


__all__ = [
    'RoleMixin', 'UserMixin', 'ApiKey',
    'roles_users'
]


# Declarative table (for generating migration files)

roles_users = sa.Table(
    'roles_users',
    Model.metadata,
    sa.Column('user_id', sa.Integer(), sa.ForeignKey('user.id')),
    sa.Column('role_id', sa.Integer(), sa.ForeignKey('role.id'))
)


# Mixin classes (import these to use in the webapp)

class RoleMixin:
    id = sa.Column(sa.Integer(), primary_key=True)
    name = sa.Column(sa.String(80), unique=True)
    description = sa.Column(sa.String(255))

    def __repr__(self):
        return f"{self.__class__.__qualname__}('{self.name}')"


class UserMixin(ActiveFlagMixin):
    id = sa.Column(sa.Integer(), primary_key=True)
    email = sa.Column(sa.String(255), unique=True, nullable=False)
    first_name = sa.Column(sa.String(255))
    last_name = sa.Column(sa.String(255))
    company_name = sa.Column(sa.String(255))
    password = sa.Column('password_hash', sa.String(128))
    confirmed_at = sa.Column(sa.DateTime())

    last_login_at = sa.Column(sa.DateTime())
    current_login_at = sa.Column(sa.DateTime())
    last_login_ip = sa.Column(sa.String(40))
    current_login_ip = sa.Column(sa.String(40))
    login_count = sa.Column(sa.Integer())

    @declared_attr
    def roles(cls):
        return sa.orm.relationship(
            'Role', secondary=roles_users,
            enable_typechecks=False,
            backref=sa.orm.backref(
                'users', enable_typechecks=False,
                lazy='dynamic')
        )

    def has_any_role(self, roles):
        if isinstance(roles, str):
            return self.has_role(roles)
        # else
        for role in roles:
            if isinstance(role, str):
                if role in [r.name for r in self.roles]:
                    return True
            elif role in self.roles:
                return True
        return False

    @property
    def is_superuser(self):
        return self.has_role('superuser')

    @property
    def is_admin(self):
        return (
            self.is_superuser
            or False
        )

    def get_preferred_name(self):
        if self.first_name:
            return self.first_name
        else:
            name, at, domain = self.email.partition('@')
            return name.split('.')[0].title()

    def has_access(self, scenario, ignore_admin=False):
        return (scenario in self.active_scenarios) or (not ignore_admin and self.is_admin)

    @property
    def joined_scenarios(self):
        scenarios = [
            p.model for p in self._scenario_permissions
            if p.level.value <= PermissionsEnum.view.value
        ]
        return scenarios

    @property
    def active_scenarios(self):
        all_scenarios = [*self.created_scenarios, *self.joined_scenarios]
        return all_scenarios

    def can(self, action, restricted_model, ignore_superuser=False):
        if not hasattr(restricted_model, '_permissions'):
            raise ValueError(
                f'{restricted_model} does not require access permissions'
            )

        if self.is_superuser and not ignore_superuser:
            return True

        return restricted_model.allows(self, action)

        return False

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.email})"


class ApiKey(Model):
    value = sa.Column(sa.Unicode(255), unique=True, nullable=False)
    active = sa.Column(sa.Boolean(), nullable=False, default=True)

    user_id = sa.Column(
        sa.Integer(), sa.ForeignKey('user.id'), nullable=False
    )
    user = sa.orm.relationship(
        'User', backref=sa.orm.backref(
            f'api_keys', cascade='all, delete-orphan'
        )
    )

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.user})"
