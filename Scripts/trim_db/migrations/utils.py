from alembic import op
import sqlalchemy as sa

def has_results(sql):
    conn = op.get_bind()
    return len(conn.execute(sa.text(sql)).all()) != 0