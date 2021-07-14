from flask_login import AnonymousUserMixin
from flask_security import UserMixin, RoleMixin
import trim_db as db


class Role(db.RoleMixin, db.Model, RoleMixin):
    __table_args__ = {'extend_existing': True}


class User(db.UserMixin, db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}


def user_factory():
    return User.query


class AnonUser(AnonymousUserMixin, User):
    __abstract__ = True

    # Just to be safe, define these again
    is_authenticated = False

    @property
    def is_superuser(self):
        return False

    @property
    def is_admin(self):
        return False
