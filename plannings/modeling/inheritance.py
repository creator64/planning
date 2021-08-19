class Inheritance:
    pass


class InheritRowToCol(Inheritance): # the rows of the parent are the same as the columns of the inheritor
    def __init__(self, parent, tablename, column):
        self.inheritor = None # the branch that inherits (will be assigned in Tree.handle_branches)
        self.parent = parent # the branch where the inheritor inherits from
        self.tablename = tablename # the tablename of the parent
        self.column = column # the name of the column of the table that gets inherited

    def __repr__(self):
        return f"InheritRowToCol(parent={self.parent.__str__()}, tablename={self.tablename}, column_of_table={self.column})"
