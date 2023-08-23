import sqlalchemy as sa
from ..utils.base import Model

__all__ = ['Chemical']


class Chemical(Model):
    name = sa.Column(sa.String(120), nullable=False)
    cas_number = sa.Column(sa.String(120), nullable=False, unique=True)

    category = sa.Column(sa.String(240))

    _scenarios = sa.orm.relationship(
        'Scenario', secondary='scenario_chemicals',
        enable_typechecks=False,
        backref=sa.orm.backref(
            '_chemicals', enable_typechecks=False
        )
    )

    @property
    def normalized_category(self):
        return self.category.replace(' |', '|').replace('| ', '|')

    def isa(self, cat_or_chem):
        if isinstance(cat_or_chem, str):
            cat_or_chem = cat_or_chem.replace(' |', '|').replace('| ', '|')
            if cat_or_chem == self.name:
                return True
            if f'|{cat_or_chem}|' in f'|{self.normalized_category}|':
                return True
        elif isinstance(cat_or_chem, Chemical):
            if cat_or_chem.id == self.id:
                return True
        else:
            raise TypeError

        return False

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'cas_number': self.cas_number,
            'category': self.category
        }

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            f'"{self.name}", {self.cas_number}'
            ')'
        )


scenario_chemicals = sa.Table(
    'scenario_chemicals',
    Model.metadata,
    sa.Column(
        'scenario_id', sa.Integer(),
        sa.ForeignKey('scenario.id')
    ),
    sa.Column(
        'chemical_id', sa.Integer(),
        sa.ForeignKey('chemical.id')
    ),
    sa.UniqueConstraint('scenario_id', 'chemical_id'),
)
