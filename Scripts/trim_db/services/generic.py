import os
from ..schema import Model
from ..schema.utils.caching import CacheManager


__all__ = ['db', 'GenericService', 'PermissionsMixin']


if os.getenv('TEST_DB_SERVERLESS'):
    from .engine import DataBase

    if 'RDS_DB_NAME' in os.environ:
        USERNAME = os.environ['RDS_USERNAME']
        PASSWORD = os.environ['RDS_PASSWORD']
        HOST = os.environ['RDS_HOSTNAME']
        PORT = os.environ['RDS_PORT']
        DBNAME = os.environ['RDS_DB_NAME']
        db_uri = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
        db = DataBase(db_uri, model_base=Model)
    elif 'SQLITE_DB_NAME' in os.environ:
        db_filename = 'database.db'
        db_path = (
            'sqlite:///'
            + f'{os.path.dirname(os.path.abspath(__file__))}/../../'
            + os.environ['SQLITE_DB_NAME']
        )
        print(f'-- Connecting to local SQLite file\n({db_path})')
        db = DataBase(db_path, model_base=Model)
    else:
        import urllib.parse
        USERNAME = os.getenv('MYSQL_USERNAME', 'root')
        PASSWORD = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD', ''))
        HOST = os.getenv('MYSQL_HOSTNAME', 'localhost')
        PORT = os.getenv('MYSQL_PORT', '3306')
        DBNAME = os.getenv('MYSQL_DB_NAME', 'pytrim')
        print(f'-- Connecting to local MYSQL db')
        db_uri = f'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}'
        db = DataBase(db_uri, model_base=Model)
else:
    print('-- Connecting to flask_sqlalchemy db')
    from flask_sqlalchemy import SQLAlchemy
    db = SQLAlchemy(model_class=Model)


def make_key(**opts):
    opts = dict(sorted(dict(opts).items()))
    key = '-'.join([
        f'{k}={v}'
        for k, v in dict(opts).items()
    ])
    return key


# Caching is currently disabled; too buggy.
# If this ends up being inefficient
# we should return to caching and fix it
class ServiceMetaClass(type):
    @property
    def db(cls):
        return db

    def cache(cls, key, value):
        try:
            cls.__cache
        except AttributeError:
            cls.__cache = {}
        cls.__cache[key] = value

    def cached(cls, key):
        try:
            cls.__cache
        except AttributeError:
            cls.__cache = {}
        # Using 'get' instead of 'pop' here would enable caching
        return cls.__cache.pop(key, None)

    def clear_cache(cls):
        cls.__cache.clear()  # = {}


class GenericService(metaclass=ServiceMetaClass):
    __model__ = None
    __unique_on__ = []

    auto_commit = True

    @classmethod
    def commit(cls, preserve_cache=False):
        if not preserve_cache:
            # cls.clear_cache()
            CacheManager.clear()
        try:
            cls.db.session.commit()
        except Exception as e:
            cls.db.session.rollback()
            print(f"Error on commit {e}")

    @classmethod
    @CacheManager.without_caching
    def create(cls, *, no_commit=False, check_unique=True, **kwargs):
        opts = dict(kwargs)

        for k in list(opts):
            opt = opts.pop(k)
            if hasattr(opt, 'id') and hasattr(cls.__model__, f'{k}_id'):
                opts[f'{k}_id'] = opt.id
            else:
                opts[k] = opt

        if check_unique and cls.__unique_on__:
            check = {k: opts.get(k) for k in cls.__unique_on__}
            existing_term = cls.get(**check)

            if existing_term:
                for k, v in kwargs.items():
                    if hasattr(existing_term, k):
                        setattr(existing_term, k, v)
                cls.db.session.add(existing_term)
                if not no_commit and cls.auto_commit:
                    cls.commit()
                return existing_term

        with cls.db.session.no_autoflush:
            model = cls.__model__(**opts)
            cls.db.session.add(model)
            # cls.cache(make_key(**opts), model)

        if not no_commit and cls.auto_commit:
            cls.commit()
        return model

    @classmethod
    def get_all(cls, **kwargs):
        # key = make_key(**kwargs)
        # if not cls.cached(key):
        with cls.db.session.no_autoflush:
            model_query = cls.db.session.query(cls.__model__)
            if kwargs:
                model_query = model_query.filter_by(**kwargs)
            models = model_query.all()
                # cls.cache(key, models)
        # ret = cls.cached(key) or []
        ret = models
        if isinstance(ret, cls.__model__):
            ret = [ret]

        with cls.db.session.no_autoflush:
            ret = [
                x if (x in cls.db.session) else cls.db.session.merge(x)
                for x in ret
            ]
        return ret

    @classmethod
    def get(cls, model_id=None, **kwargs):
        ret = None
        query_options = kwargs.pop('query_options', None)
        if model_id is not None:
            if not isinstance(model_id, int):
                try:
                    model_id = int(model_id)
                except Exception:
                    raise TypeError(
                        '"model_id" must be of type int,'
                        f' not {model_id.__class__.__name__}'
                    )
            if model_id > 0:
                # if not cls.cached(model_id):
                with cls.db.session.no_autoflush:
                    q = cls.db.session.query(cls.__model__)
                    if query_options is not None:
                        q = q.options(query_options)
                    model = q.get(
                        model_id
                    )
                    # cls.cache(model_id, model)
                # ret = cls.cached(model_id)
                ret = model
        elif kwargs:
            models = cls.get_all(**kwargs)
            models.append(None)
            ret = models[0]

        if ret:
            with cls.db.session.no_autoflush:
                if ret not in cls.db.session:
                    ret = cls.db.session.merge(ret)
        return ret

    @classmethod
    def get_or_create(cls, model_id=None, no_commit=False, **kwargs):
        check_unique = kwargs.pop('check_unique', False)
        create_kwargs = kwargs.pop('create_kwargs', None)
        model = cls.get(model_id=model_id, **kwargs)
        if model is None:
            if create_kwargs:
                kwargs.update(create_kwargs)
            model = cls.create(
                no_commit=no_commit, check_unique=check_unique, **kwargs
            )
        with cls.db.session.no_autoflush:
            if model not in cls.db.session:
                model = cls.db.session.merge(model)
        return model

    @classmethod
    def update(cls, model):
        if isinstance(model, list):
            models = model
        else:
            models = [model]

        for model in models:
            if not isinstance(model, cls.__model__):
                raise TypeError(
                    '"model" must be of type'
                    f' {cls.__model__.__class__.__name__},'
                    f' not {model.__class__.__name__}'
                )
            if model in cls.db.session:
                cls.db.session.expunge(model)
        cls.db.session.add_all(models)
        cls.commit()

    @classmethod
    def delete(cls, model_or_id, no_commit=False):
        CacheManager.clear()
        if isinstance(model_or_id, int):
            model = cls.get(model_or_id)
        elif isinstance(model_or_id, cls.__model__):
            model = model_or_id
            if model not in cls.db.session:
                model = cls.db.session.merge(model)
        else:
            raise TypeError(
                '"model_or_id" must be of type int'
                f' or {cls.__model__.__class__.__name__},'
                f' not {model_or_id.__class__.__name__}'
            )

        cls.db.session.delete(model)
        if not no_commit and cls.auto_commit:
            cls.commit()

    def __init__(self, model, *args, **kwargs):
        self.__instance = model


class PermissionsMixin:
    @classmethod
    def grant(cls, model, user, permission, no_commit=False):
        if not hasattr(model, 'grant'):
            raise TypeError(
                f'{model.__class__.__qualname__} does not support permissions'
            )
        model.grant(user, permission)
        cls.db.session.add(model)
        if not no_commit and cls.auto_commit:
            cls.commit()

    @classmethod
    def clear_permissions(cls, model, except_for=[]):
        model._permissions = [  # Clear existing permissions
            x for x in model._permissions if x.user_id in except_for
        ]
