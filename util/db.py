"""Raw SQL-based Postgres DB (R)ead management (use an ORM for CUD)"""

import psycopg
from util import conf
from psycopg_pool import ConnectionPool
from psycopg.rows import namedtuple_row

conninfo =  f'host={conf.PostGres.db_host} '\
            f'port={conf.PostGres.db_port} '\
            f'dbname={conf.PostGres.db_textgen} '\
            f'user={conf.PostGres.db_user} '\
            f'password={conf.PostGres.db_pswd}'

pool = ConnectionPool(conninfo=conninfo, min_size=2, open=False)


def raw_sql(psycopg_sql_string, **kwargs) -> list:
    """ Perform SQL select query using a psycopg3 style SQL statement.
        Returns the list of selected rows.
    """
    if pool.closed:
        pool.open()
        pool.wait()

    with pool.connection() as conn:
        conn.autocommit = True
        conn.row_factory = namedtuple_row
        cur : psycopg.Cursor = conn.cursor()
        rows = cur.execute(query=psycopg_sql_string, params=kwargs).fetchall()
    
    return rows
