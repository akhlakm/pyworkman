""" Raw SQL-based Postgres DB I/O utils """

import psycopg
from util import conf
from datetime import datetime
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
    if pool.closed: pool.open()

    with pool.connection() as conn:
        conn.autocommit = True
        conn.row_factory = namedtuple_row
        cur : psycopg.Cursor = conn.cursor()
        rows = cur.execute(query=psycopg_sql_string, params=kwargs).fetchall()
    
    return rows


class Table:
    def __init__(self, _tableName, **cols) -> None:
        """ Generic table definition for creating and inserting.
            Example:
                tabl = Table("test",
                    name = "varchar NOT NULL UNIQUE",
                    age  = "int4 NOT NULL"
                )
        """
        self.name = _tableName
        self.pkey = 'id'
        self.columns = {
            "id": f"int4 NOT NULL GENERATED BY DEFAULT AS IDENTITY(INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1 NO CYCLE)",
            "date_added": "timestamptz NOT NULL",
        }
        self._indices = {}
        self._constraints = {"id": f"{self.name}_pkey PRIMARY KEY"}

        for k, v in cols.items():
            self.columns[k] = v

    def __repr__(self) -> str:
        r = f"Table {self.name}({', '.join([k for k in self.columns.keys()])})"
        return r

    def constraint(self, col : str, value : str):
        self._constraints[col] = value

    def index(self, col : str, ops : str = None):
        if ops: assert ops in ['varchar', 'text']
        self._indices[col] = f"{ops}_pattern_ops" if ops else ""

    def _create_sql(self) -> str:
        sql = f"CREATE TABLE IF NOT EXISTS {self.name} (\n\t"
        rows = [f'"{k}" {v}' for k, v in self.columns.items()]
        rows += [f'CONSTRAINT {v} ("{k}")' for k, v in self._constraints.items()]
        sql += ",\n\t".join(rows) + "\n);"
        return sql
    
    def _index_sql(self) -> list[str]:
        return [
            f'CREATE INDEX IF NOT EXISTS ix_{self.name}_{k} ON {self.name} USING btree ("{k}" {v});'
            for k, v in self._indices.items()
        ]
    
    def create_all(self, drop_existing = False):
        """ Create the table and all the defined indices.
        """
        if pool.closed: pool.open()
        with pool.connection() as conn:
            try:
                if drop_existing:
                    for k in self._indices.keys():
                        sql = f"DROP INDEX IF EXISTS ix_{self.name}_{k};"
                        conn.execute(sql)

                    sql = f"DROP TABLE IF EXISTS {self.name};"
                    conn.execute(sql)

                for sql in [self._create_sql()] + self._index_sql():
                    print(sql)
                    conn.execute(sql)

                conn.commit()

            except:
                conn.rollback()
                raise

    def insert_row(self, **kwargs):
        """ Insert a single table row and commit immediately.
            Returns the inserted Row with the id field. Example:
            tabl.insert_row(name = "John", age = 31)
        """
        if "date_added" not in kwargs:
            kwargs["date_added"] = datetime.now()

        columns = [k for k in kwargs.keys()]
        for col in columns:
            assert col in self.columns, f"Column '{col}' not in {self}"

        column_string = ", ".join(columns)
        values_string = ", ".join([f"%({k})s" for k in columns])

        sql = f"""
        INSERT INTO {self.name} ({column_string})
        VALUES ({values_string}) RETURNING id;
        """
        row = raw_sql(sql, **kwargs)

        if row:
            return row[0]
        return None

    def copy(self, rows : list[dict]):
        """ Insert a batch of rows and commit at the end. Example:
            tabl.copy([
                {'name': "Mike", 'age': 23},
                {'name': "Kate", 'age': 41},
                {'name': "Terry", 'age': 9},
            ])
        """
        columns = [k for k in rows[0].keys()]
        if "date_added" not in columns:
            columns.append('date_added')

        for col in columns:
            assert col in self.columns, f"Column '{col}' not in {self}"

        column_string = ", ".join(columns)
        sql = f"COPY {self.name} ({column_string}) FROM STDIN"

        if pool.closed: pool.open()
        with pool.connection() as conn:
            cur : psycopg.Cursor = conn.cursor()
            try:
                with cur.copy(sql) as copy:
                    for row in rows:
                        if 'date_added' not in row:
                            row['date_added'] = datetime.now()
                        copy.write_row([row[k] for k in columns])

                conn.commit()
            except:
                conn.rollback()
                raise


if __name__ == "__main__":
    tabl = Table("test",
        name   = "varchar NOT NULL UNIQUE",
        age    = "int4 NOT NULL"
    )

    tabl.index('age')
    tabl.index('name', 'varchar')
    tabl.create_all(drop_existing=True)

    print(tabl.insert_row(name = "John", age = 31))
    print(tabl.insert_row(name = "Doe", age = 32))

    tabl.copy([
        {'name': "Mike", 'age': 23},
        {'name': "Kate", 'age': 41},
        {'name': "Terry", 'age': 9},
    ])

    for row in raw_sql("SELECT * FROM test;"):
        print(row)

    print("Done")
