
def implement_users_roles():
    """
    We don't implement these by default, because the webapp
    needs to extend the mixin with stuff for Flask-Security
    -- but they need a default implementation to generate
    migrations, so just build that on the fly.
    """
    try:
        from trim_db.schema.utils.base import Model
        from trim_db.schema.users.models import RoleMixin, UserMixin
    except Exception:
        from schema.utils.base import Model
        from schema.users.models import RoleMixin, UserMixin
    print("-- Creating dummy User/Role ORM")

    class Role(RoleMixin, Model):
        pass

    class User(UserMixin, Model):
        pass

    return Role, User
