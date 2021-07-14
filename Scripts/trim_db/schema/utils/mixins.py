import sqlalchemy as sa
from datetime import datetime
from .base import QueryBase


class TrackUpdatesMixin:
    created = sa.Column(
        sa.DateTime(), nullable=False, default=datetime.utcnow
    )
    updated = sa.Column(
        sa.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow
    )


# https://blog.miguelgrinberg.com/post/implementing-the-soft-delete-pattern-with-flask-and-sqlalchemy
# WARNING:  If you use this custom query class in a sa.relationship()
# to enable soft-deletion, you MUST call .all() on the returned value
# everywhere you need to access it
# (Unless you use with_inactive() ... maybe ...)
class OnActiveQuery(QueryBase):
    _with_inactive = False

    def __new__(cls, *args, **kwargs):
        obj = super().__new__(cls)
        obj._with_inactive = kwargs.get('_with_inactive', False)
        if len(args) > 0 and not obj._with_inactive:
            obj.__init__(*args, **kwargs)
            return obj.filter_by(active=True)
        return obj

    def __init__(self, *args, **kwargs):
        self._with_inactive = kwargs.pop('_with_inactive', False)
        super().__init__(*args, **kwargs)

    def with_inactive(self):
        return self.__class__(sa.class_mapper(self._mapper_zero().class_),
                              session=sa.session(), _with_inactive=True)

    def _get(self, *args, **kwargs):
        # this calls the original query.get function from the base class
        return super().get(*args, **kwargs)

    def get(self, *args, **kwargs):
        # the query.get method does not like it if there is a filter clause
        # pre-loaded, so we need to implement it using a workaround
        obj = self.with_inactive()._get(*args, **kwargs)
        if obj is None or self._with_inactive or obj.active:
            return obj
        return None


class ActiveFlagMixin:
    query_class = OnActiveQuery
    active = sa.Column(sa.Boolean(), nullable=False, default=True)
