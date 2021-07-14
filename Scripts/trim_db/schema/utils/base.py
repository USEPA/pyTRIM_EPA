import re
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base, declared_attr


camelcase_re = re.compile(r'([A-Z]+)(?=[a-z0-9])')


def camel_to_snake_case(name):
    def _join(match):
        word = match.group()

        if len(word) > 1:
            return ('_%s_%s' % (word[:-1], word[-1])).lower()

        return '_' + word.lower()

    return camelcase_re.sub(_join, name).lstrip('_')


class QueryBase(sa.orm.Query):
    pass


class ModelBase:
    @declared_attr
    def __tablename__(cls):
        return camel_to_snake_case(cls.__name__)

    @declared_attr
    def id(cls):
        return sa.Column(
            sa.Integer(), primary_key=True, autoincrement=True
        )

    def __repr__(self):
        return f"{self.__class__.__qualname__}({self.id})"


Model = declarative_base(cls=ModelBase, name='Model')
