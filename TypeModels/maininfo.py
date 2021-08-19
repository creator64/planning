from plannings.modeling.tree import Tree
from plannings.modeling.tablemodel import TableModel
from plannings.database.utils import CurrentTime
from sqlalchemy import Integer, String, Boolean, DateTime, Date, Column

# this file represents how the maindata is stored

class Main(Tree):
    tables = [
                TableModel("applications", Column("id", Integer, primary_key=True),
                                           Column("name", String), Column("type", String),
                                           Column("date", Date, server_default=CurrentTime), Column("version", String))
             ]
    name = "Main"


Tree.handle_branches()
