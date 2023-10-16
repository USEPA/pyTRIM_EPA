from trim_db.utils.users_roles import implement_users_roles

__all__ = []


try:
    implement_users_roles()
except Exception as e:
    print(f'-- Unable to create Users/Roles.\n{e}')
