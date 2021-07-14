from flask import Blueprint, request
from .responses import ApiResult, ApiException


class CrudBlueprint(Blueprint):
    @staticmethod
    def make_get_all(cls, session):
        def get_all():
            q = session.query(cls).all()
            return ApiResult(q)
        return get_all

    @staticmethod
    def make_get_single(cls, session):
        def get_single(pk):
            q = session.query(cls).get(pk)
            return ApiResult(q)
        return get_single

    @staticmethod
    def make_create(cls, session):
        def create():
            try:
                kwargs = {**request.args, **request.json}
                n = cls(**kwargs)
                session.add(n)
                session.commit()
                return ApiResult({
                    'message': 'success',
                    'id': n.id
                })
            except Exception as e:
                raise ApiException(str(e))
        return create

    @staticmethod
    def make_update(cls, session):
        def update(pk):
            try:
                q = cls.query.get(pk)
                if q:
                    kwargs = {**request.args, **request.json}
                    for k, v in kwargs.items():
                        if k == 'id' or not hasattr(q, k):
                            continue
                        setattr(q, k, v)
                    session.commit()
                return ApiResult({
                    'message': 'success',
                    'id': q.id
                })
            except Exception as e:
                raise ApiException(str(e))
        return update

    @staticmethod
    def make_delete(cls, session):
        def delete(pk):
            try:
                q = cls.query.get(pk)
                if q:
                    session.delete(q)
                    session.commit()
                return ApiResult({
                    'message': 'success',
                    'id': q.id
                })
            except Exception as e:
                raise ApiException(str(e))
        return delete

    def __init__(
        self, cls, import_name, session=None, *args,
        name=None, url_prefix=None,
        can_create=True, can_update=True, can_delete=True,
        view_only=False,
        **kwargs
    ):
        if session is None:
            raise TypeError(
                'Cannot initialize CRUD Blueprint '
                'without a database session.'
            )

        cls_name = cls.__qualname__.lower()
        name = name or f'api.{cls_name}'
        url_prefix = url_prefix or f'/api/{cls_name}'
        super().__init__(
            name, import_name, *args,
            url_prefix=url_prefix, **kwargs
        )

        self.get_all = self.route('/')(
            self.make_get_all(cls, session)
        )
        self.get_single = self.route('/<int:pk>')(
            self.make_get_single(cls, session)
        )

        if not view_only and can_create:
            self.create = self.route(
                '/', methods=['POST']
            )(
                self.make_create(cls, session)
            )

        if not view_only and can_update:
            self.update = self.route(
                '/<int:pk>', methods=['PUT', 'PATCH']
            )(
                self.make_update(cls, session)
            )

        if not view_only and can_delete:
            self.delete = self.route(
                '/<int:pk>', methods=['DELETE']
            )(
                self.make_delete(cls, session)
            )
