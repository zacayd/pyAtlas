from sqlalchemy import create_engine
import pandas as pd
from sqlalchemy import text

class DataAccessLayer:
    def __init__(self, db_uri):
        server=db_uri.split(';')[0].split('=')[1]
        database = db_uri.split(';')[1].split('=')[1]
        usr = db_uri.split(';')[2].split('=')[1]
        pwd = db_uri.split(';')[3].split('=')[1]
        conn_string = f"mssql+pyodbc://{usr}:{pwd}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        try:
            self.engine = create_engine(conn_string)
        except Exception as e:
            print(e)

    def execute_query(self, query,connectionid):
        with self.engine.connect() as conn:
            try:
                query=query.replace("?",connectionid)

                df = pd.read_sql(text(query), conn)
                conn.close()

            except Exception as e:
                print(e)
        return df
