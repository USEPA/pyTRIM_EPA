import sqlalchemy as sa
from enum import Enum
from .base import Model
from .types import IntEnum
from .serialize import register_serializer


__all__ = [
    'PermissionsEnum', 'require_permissions'
]


class PermissionsEnum(Enum):
    manage = 1
    edit = 10
    view = 100
    none = 666

    @staticmethod
    def entails(parent, child):
        if PermissionsEnum[parent].value < PermissionsEnum[child].value:
            return True

        return False


@register_serializer(PermissionsEnum)
def serialize_permissions_enum(e: PermissionsEnum):
    return e.name


def require_permissions(*args, **kwargs):
    allow_keys = kwargs.get('allow_keys') or {}
    for k, v in list(allow_keys.items()):
        if isinstance(v, str):
            allow_keys[k] = PermissionsEnum[v]
        v = allow_keys[k]
        if not isinstance(v, PermissionsEnum):
            raise ValueError(f'Invalid permissions level: {v}')

    def define_permissions_table(cls):
        tbl = cls.__tablename__

        class Permissions(Model):
            __tablename__ = f'{tbl}_permissions'

            user_id = sa.Column(
                sa.Integer(), sa.ForeignKey('user.id'), nullable=False
            )
            user = sa.orm.relationship(
                'User', backref=sa.orm.backref(
                    f'_{tbl}_permissions', cascade='all, delete-orphan'
                )
            )

            model_id = sa.Column(
                f'{tbl}_id', sa.Integer(), sa.ForeignKey(f'{tbl}.id'),
                nullable=False
            )

            level = sa.Column(
                IntEnum(PermissionsEnum),
                nullable=False, default=PermissionsEnum.none
            )

            __table_args__ = (
                sa.UniqueConstraint('user_id', f'{tbl}_id'),
            )

            def __repr__(self):
                return f'{cls.__name__}Permissions({self.user}, {self.level})'

        cls._permissions = sa.orm.relationship(
            Permissions,
            cascade='all, delete-orphan',
            backref=sa.orm.backref('model')
        )

        def access_level(s, user):
            if not isinstance(user, int):
                user = user.id
            if allow_keys:
                for key, level in allow_keys.items():
                    try:
                        val = getattr(s, key)
                        if not isinstance(val, int):
                            val = val.id
                        if val == user:
                            return level
                    except Exception:
                        pass
            p = [x for x in s._permissions if x.user_id == user]
            if not p:
                return None
            return p[0].level

        cls.access_level = access_level

        def grant(s, user, permission):
            if not isinstance(user, int):
                user = user.id
            if permission is None:
                s._permissions = [  # Clear existing permissions
                    x for x in s._permissions if x.user_id != user
                ]
                return None
            if not isinstance(permission, Enum):
                permission = PermissionsEnum[permission]
            p = [x for x in s._permissions if x.user_id == user]
            if p:
                return p[0]
            perm = Permissions(user_id=user, level=permission)
            s._permissions.append(perm)
            return perm

        cls.grant = grant

        def revoke(s, user, permission=None):
            if permission is None:
                return s.grant(user, None)
            raise NotImplementedError()

        cls.revoke = revoke

        custom_allow = kwargs.get('custom_allow')
        if custom_allow is None:
            def custom_allow(s, u):
                return False

        def allows(s, user, action):
            if isinstance(action, str):
                action = PermissionsEnum[action].value
            elif isinstance(action, Enum):
                action = action.value
            if not isinstance(action, int):
                raise ValueError(f'Invalid action: {action}')
            if custom_allow(s, user):
                return True
            if allow_keys:
                for key, level in allow_keys.items():
                    try:
                        val = getattr(s, key)
                        if not isinstance(val, int):
                            val = val.id
                        if val == user.id and level.value <= action:
                            return True
                    except Exception:
                        pass
            for p in s._permissions:
                if (p.user_id == user.id) and (p.level.value <= action):
                    return True
            return False

        cls.allows = allows

        return cls
    
    if kwargs or len(args) > 1:
        return define_permissions_table
    else:
        return define_permissions_table(args[0])
