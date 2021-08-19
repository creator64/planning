from plannings.screens.dynamic_screen import DynamicScreen
import os

class Tree:
    master = None # the parent branch: when the parent branch is created this branch gets created too
    children: list = [] # the children of a branch (see master): will be assigned in Tree.handle_branches()
    name: str = None # name of a branch showed in the gui
    tables: list = [] # list of tables that will be created when this branch is created
    screens: dict = {} # screens that belong to a branch
    find_screen: bool = False # doesnt do anything yet
    istype: bool = False # indicates if the branch is a planningtype
    menuscreen: DynamicScreen = None # when opening certain application type this screen will show up
    createscreen: DynamicScreen = None # when creating this type, this screen will show up

    def __str__(self):
        return f"Tree object named {self.name}"

    @staticmethod
    def handle_branches():
        branches = Tree.__subclasses__()
        for branch in branches:
            branch.children = branch._get_children() # assign the children of each branch
            branch._fix_tables() # assign to the table to which branch it belongs
            branch._fix_screens() # assign to the screens to what branch it belongs

    @classmethod
    def _get_children(self):
        children = []
        branches = Tree.__subclasses__()
        for branch in branches:
            if branch.master == self:
                children.append(branch)
        return children

    @classmethod
    def _fix_tables(self):
        for table in self.tables:
            table.branch = self # assign branch(self) as master to all the tables of a branch

    @classmethod
    def _fix_screens(self):
        for screen in self.screens:
            self.screens[screen].branch = self
        if self.menuscreen: self.menuscreen.branch = self
        if self.createscreen: self.createscreen.branch = self

    def get_table(self, name):
        for table in self.tables:
            if table.tablename == name:
                return table
        return None

    @classmethod
    def get_tablename(self, table: "str or TableModel object", applid=None):
        tbn = str(table)
        if applid: return "_".join([self.get_path(), tbn, str(applid)])
        return "_".join([self.get_path(), tbn])

    @classmethod
    def get_path(self):
        master = self.master # get master of branch
        branch_list = [self.name if self.name else self.__class__.__name__] # add name of the branch
        while(master): # add names of all masters
            branch_list.append(master.name if master.name else master.__class__.__name__)
            master = master.master
        branch_list.reverse() # reverse so the ultimate masters name is the first of the list
        return "_".join(branch_list)

    @classmethod
    def create(self, dbconn, applid=None, create_children=True):
        return dbconn.create_branch(self, applid=applid, create_children=create_children) # shortcut for DB.create_branch()

    @classmethod
    def load(self, dbconn, applid=None, ORDER_BY={}, WHERE={}):
        return dbconn.load_branch(self, applid=applid, ORDER_BY=ORDER_BY, WHERE=WHERE) # shortcut for DB.load_branch()

    @classmethod
    def delete(self, dbconn, applid=None, delete_children=True):
        return dbconn.delete_branch(self, applid=applid) # shortcut for DB.delete_branch()
