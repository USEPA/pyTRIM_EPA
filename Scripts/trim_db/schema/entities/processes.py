import numpy as np
import sqlalchemy as sa
from ..parameters.equations import as_function
from ..utils.base import Model
from ..utils.caching import CacheManager


__all__ = [
    'TransportProcess'
]


class TransportProcess(Model):
    name = sa.Column(sa.String(240), nullable=False, unique=True)

    algorithm_id = sa.Column(
        sa.Integer(), sa.ForeignKey('formula.id'), nullable=False
    )
    algorithm = sa.orm.relationship('Formula')

    category = sa.Column(sa.String(240), default='Transport', nullable=False)

    requirements = sa.Column(sa.String())

    output_chemical_id = sa.Column(
        sa.Integer(), sa.ForeignKey('chemical.id')
    )
    output_chemical = sa.orm.relationship('Chemical')

    @property
    def is_transform(self):
        return self.category.startswith('Transform')

    def applies_to(self, **kwargs):
        if not self.requirements:
            return True

        if not hasattr(self, '_validator'):
            setattr(self, '_validator', as_function(self.requirements))
        return self._validator(**kwargs) or False

    def evaluate(self, **kwargs):
        @CacheManager.with_caching(f'transport_process::{self.id}')
        def cached_eval(**kwargs):
            if not self.applies_to(**kwargs):
                raise TypeError(
                    f'Invalid arguments for "{self.name}": {kwargs}'
                )
            try:
                return self.algorithm.evaluate(IGNORE_EXTRA=True, **kwargs)
            except Exception as e:
                if 'Missing argument' in str(e):
                    raise
                raise
                return np.nan
        return cached_eval(**kwargs)

    def eval(self, **kwargs):
        return self.evaluate(**kwargs)

    def __repr__(self):
        return (
            f'{self.__class__.__qualname__}('
            + f'"{self.category}", "{self.algorithm.equation}"'
            + (f', "{self.requirements}"' if self.requirements else '')
            + (
                f' > "{self.output_chemical.name}"'
                if self.output_chemical else ''
            )
            + ')'
        )
