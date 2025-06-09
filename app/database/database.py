import pandas as pd
import psycopg2
from sqlalchemy import create_engine

class DatabaseConnection:
    def __init__(self):
        
        self.conn = psycopg2.connect(
            host="192.168.180.44",
            port="5434",
            database="dados_importados",
            user="postgres",
            password="1234"
        )
        self.engine = create_engine("postgresql+psycopg2://postgres:1234@192.168.180.44:5434/dados_importados")

        self.conn = psycopg2.connect(
            host="192.168.180.44",
            port="5434",
            database="postgres",
            user="postgres",
            password="1234"
        )
        self.engineTst = create_engine("postgresql+psycopg2://postgres:1234@192.168.180.44:5434/postgres")


    def load_dataframe(self, query):
        return pd.read_sql(query, self.engine).dropna()

    def load_dataframeTeste(self, query):
        return pd.read_sql(query, self.engineTst).dropna()
