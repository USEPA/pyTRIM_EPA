import sqlalchemy as sa
from ..utils.base import Model
from ..utils.mixins import TrackUpdatesMixin


__all__ = [
    'Scenario', 'Team'
]


class Scenario(Model, TrackUpdatesMixin):
    name = sa.Column(sa.String(120), nullable=False)
    description = sa.Column(sa.String(255))

    @property
    def safe_name(self):
        return self.name.replace(' ', '_')

    @property
    def short_description(self):
        if not self.description:
            return ''

        w = self.description.split()
        w.reverse()
        short = ''
        while len(short) < 75 and len(w):
            short += ' ' + w.pop()
        if len(w):
            short += ' ...'
        return short.strip()

    creator_id = sa.Column(
        sa.Integer(), sa.ForeignKey('user.id'), nullable=False
    )
    creator = sa.orm.relationship(
        'User', backref=sa.orm.backref('created_scenarios', lazy='dynamic')
    )

    team_members = sa.orm.relationship(
        'User', secondary='team',
        backref=sa.orm.backref('joined_scenarios', lazy='dynamic')
    )

    @property
    def team(self):
        all_members = [self.creator, *self.team_members]
        return all_members

    def as_serializable(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }


class Team(Model):
    scenario_id = sa.Column(
        sa.Integer(), sa.ForeignKey('scenario.id'), primary_key=True
    )
    scenario = sa.orm.relationship(
        'Scenario', overlaps='joined_scenarios, team_members'
    )

    member_id = sa.Column(
        sa.Integer(), sa.ForeignKey('user.id'), primary_key=True
    )
    member = sa.orm.relationship(
        'User', overlaps='joined_scenarios, team_members'
    )

    # Each user should have only one position per project
    __table_args__ = (
        sa.UniqueConstraint('scenario_id', 'member_id'),
    )
