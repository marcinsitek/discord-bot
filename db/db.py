from typing import Tuple

import pandas as pd
import psycopg2
from psycopg2.extensions import connection

class DBClient:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.dbname: str = dbname
        self.user: str = user
        self.password: str = password
        self.host: str = host

    def _connect(self) -> connection:
        return psycopg2.connect(
            dbname=self.dbname, 
            user=self.user, 
            password=self.password,
            host=self.host
        )
    
    def retrieve(self, query: str) -> pd.DataFrame:
        conn = self._connect()
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        columns = [column[0] for column in cur.description]
        conn.close()
        return pd.DataFrame.from_records(rows, columns=columns)


    def insert(self, rows: list[Tuple], schema: str, table: str) -> None:
        conn = self._connect()
        cur = conn.cursor()
        sql = "insert into {}.{} values {}".format(
            schema, table, ",".join(["%s"] * len(rows))
        )
        cur.execute(sql, rows)
        conn.commit()
        conn.close()
