from sqlalchemy import MetaData, create_engine
from plannings.database.tablecollection import TableCollection
from plannings.screens.screenmanager import ScreenManager

r"C:\Users\Armani\AppData\Local\Programs\Tesseract-OCR"

class DB:
    def __init__(self, path, sm=None):
        self.engine = create_engine(f'sqlite:///{path}')
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        self.conn = self.engine.connect()
        self.sm = sm

    def __eq__(self, o):
        if not isinstance(o, DB): return False
        if o.engine == self.engine:
            return True
        return False

    def create_branch(self, branch, applid=None, create_children=True):
        for table in branch.tables: # go through all tablemodels
            t = table.to_table(self.meta, applid=applid) # convert them to a sqlalchemy table object with the metadata
        self.meta.create_all(self.engine) # create all tables
        if create_children:
            for child in branch.children: # children are branch objects
                self.create_branch(child, applid=applid) # recursively add the children of the branch

    def load_branch(self, branch, applid=None, ORDER_BY={}, WHERE={}) -> TableCollection:
        return TableCollection(self, branch=branch, applid=applid, ORDER_BY=ORDER_BY, WHERE=WHERE)

    def delete_branch(self, branch, applid=None, delete_children=True):
        for table in branch.tables: # table is a TableModel object
            tablename = branch.get_tablename(table, applid=applid)
            self.engine.execute(f"DROP TABLE '{tablename}'")
        if delete_children:
            for child in branch.children:
                self.delete_branch(child, applid=applid)
        return 1
