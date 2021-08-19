from sqlalchemy import create_engine, MetaData
from plannings.database.table import Table
from plannings.database.where import WHERE as w

class TableCollection:
    def __init__(self, dbconn, branch=None, applid=None, tablenames=[], ORDER_BY={}, WHERE={}):
        self.branch = branch
        self.tables = []
        self.dbconn = dbconn
        self.applid = applid
        for tablename in tablenames:
            ob = ORDER_BY.get(tablename); wh = WHERE.get(tablename) # if tablename not in ORDER_BY/WHERE it returns None
            if not ob: ob = () # so we replace it with an empty tuple
            if not wh: wh = w() # so we replace it with an empty where object
            self.tables.append(Table(tablename, self.dbconn, ORDER_BY=ob, WHERE=wh))
        if branch:
            for table in branch.tables: # table is a tablemodel
                ob = ORDER_BY.get(table.tablename); wh = WHERE.get(table.tablename) # if tablename not in ORDER_BY/WHERE it returns None
                if not ob: ob = () # so we replace it with an empty tuple
                if not wh: wh = w() # so we replace it with an empty where object
                tablename = self.branch.get_tablename(table, applid=self.applid)
                self.tables.append(Table(tablename, self.dbconn, ORDER_BY=ob, WHERE=wh))

    def __getitem__(self, tbn):
        for table in self.tables: # go through all (Planning) Table objects in the collection
            if table.name == tbn: # if its name equals to given tbn we return table
                return table
            if self.branch: # if a branch is given check if tbn is can be formatted by branch.get_tablename
                if table.name == self.branch.get_tablename(tbn, applid=self.applid):
                    return table
