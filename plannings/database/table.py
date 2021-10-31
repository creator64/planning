from plannings.database.where import WHERE
from _thread import *
import pandas as pd

class Table:
    def __init__(self, name, dbconn, ORDER_BY=(), WHERE=WHERE()):
        self.name = name # name of the table
        self.dbconn = dbconn # DB object the table is connected to; contains the engine
        self.tablesqla = self.dbconn.meta.tables[self.name] # a Table object of sqlalchemy
        wh = WHERE.handle_statements(self.tablesqla) # returns a list of statements
        query = self.tablesqla.select().where(*wh).order_by(*ORDER_BY) # a select statement
        self.data = list(self.dbconn.conn.execute(query)) # the actual table data
        # IMPORTANT: DO NOT REMOVE list()

    def _repr__(self):
        print(f"table object called {self.name}\ndata:")
        for row in self.data:
            print(row)
        return ""

    def __eq__(self, o):
        if not isinstance(o, Table): return False
        if o.name == self.name and o.dbconn == self.dbconn:
            return True
        return False

    def handle_updates(f):
        def wrapper(table, *args, **kwargs): # whenever we update a table this function runs
            v = f(table, *args, **kwargs)
            # if no sm assigned to dbconn it is pointless to update screens and if we dont want to update screens we give keyword arg update_screens=False
            if (not table.dbconn.sm) or kwargs.get("update_screens") == False:
                return None
            table.dbconn.sm.update_screens(table)
            return v
        return wrapper

    @handle_updates
    def add_row(self, update_screens=True, **values: "col1=val1, col2=val2, ..."):
        st = self.tablesqla.insert().values(**values) # generate a statement
        self.dbconn.conn.execute(st) # execute the statement
        return 1

    @handle_updates
    def delete_row(self, WHERE=WHERE(), delete_table=False, update_screens=True):
        if not WHERE and not delete_table: # preventing to delete the whole table
            print("function Table.remove_row stopped becuase there were no conditions given and delete_table was set to False")
            return None
        wh = WHERE.handle_statements(self.tablesqla)
        st = self.tablesqla.delete().where(*wh) # generate a statement
        self.dbconn.engine.execute(st) # execute the statement
        return 1

    @handle_updates
    def update(self, WHERE=WHERE(), update_screens=True, **col_values: "col1=val1, col2=val2, ..."):
        wh = WHERE.handle_statements(self.tablesqla)
        st = self.tablesqla.update().values(**col_values).where(*wh)
        self.dbconn.engine.execute(st)
        return 1

    def add_col(self, new_col, TYPE="VARCHAR", default="NULL"):
        self.dbconn.engine.execute(f"ALTER TABLE {self.name} ADD {new_col} {TYPE} DEFAULT {default}")
        return 1

    def rename_col(self, col, new_col):
        self.dbconn.engine.execute(f"ALTER TABLE {self.name} RENAME COLUMN '{col}' TO '{new_col}'")
        return 1

    def check_value_exist_in_col(self, col: str, value):
        for record in self.data:
            if record[col] == value:
                return True
        return False
