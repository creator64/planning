from sqlalchemy import Table, Column, MetaData, Integer
from tabulate import tabulate

class TableModel:
    def __init__(self, tablename, *cols):
        self.tablename = tablename # tablename
        self.cols = cols # list of columns
        self.branch = None # the branch the table belongs to: will be assigned in Tree.handle_branches()

    def __repr__(self):
        table = {"Columns": self.cols.keys(), "Type": self.cols.values()}
        return f"TableModel object named {self.tablename}\n\n" + tabulate(table, headers="keys") + "\n"

    def __str__(self):
        return self.tablename

    def to_table(self, meta: MetaData, applid=None):
        return Table(self.branch.get_tablename(self.tablename, applid=applid), meta, *self.cols)
