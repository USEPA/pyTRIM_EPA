import argparse
from sqlalchemy import text
from trim_db.services.generic import db

__all__ = ['run_migration']


def run_migration(sql_path):
    print('Running migrations ...')
    dialect = active_sql_dialect()

    with open(sql_path, encoding='utf-8') as f:
        q = f.read()

    with db.engine.connect() as con:
        for x in q.split(';'):
            try:
                con.execute(text(x))
            except Exception as e:
                print(e)
    db.engine.dispose()


def active_sql_dialect():
    return str(db.engine.url).replace('\\', '/').split(':///', 1)[0]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--sql')
    args = parser.parse_args()

    run_migration(args.sql)

    print('Done!')
