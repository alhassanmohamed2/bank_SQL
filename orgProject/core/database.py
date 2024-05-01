import sqlite3
from datetime import datetime

class Database:
    def __init__(self, database_name):
        self.database_name = database_name
        self.conn = sqlite3.connect(f'{self.database_name}.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
                
    def create_table(self, table_name = "", columns= {}):
        try:
            columns_const = ', '.join(f"{name} {type}" for name, type in columns.items())
            sql = f""" CREATE TABLE {table_name}({columns_const}) """ 
            self.cursor.execute(sql)
        except Exception:
            print("Error in Table Creation")

    def select_all(self, table_name = "", columns=[], conditions={}, operators = []):
        try:
            operators = iter(operators)
            cloums_const = ', '.join(name for name in columns)
            conditions_const = f' ? '.join(f"{column} = {condition}" for column, condition in conditions.items())
            pass
        except Exception:
            print("Error in retriving data")

        pass
    def __del__(self):
        self.conn.close()


