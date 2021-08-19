from plannings.modeling.tree import Tree
from plannings.modeling.tablemodel import TableModel
from screens.testtype.menuscreen import MenuScreen_TestType
from screens.testtype.createscreen import CreateScreen_TestType
from sqlalchemy import Integer, String, Boolean, Date, Time, Column

class TestType(Tree):
    name = "Task planning"
    istype = True
    tables = [
                TableModel("tasks", Column("task", String), Column("timeneeded", Integer), Column("done", Boolean)),
                TableModel("persons", Column("name", String), Column("age", Integer), Column("workedtime", Integer))
             ]
    menuscreen = MenuScreen_TestType
    createscreen = CreateScreen_TestType

class TestType_TPD(Tree):
    master = TestType
    name = "Time per day"
    tables = [
                TableModel("timeperday", Column("day", Date), Column("task", String), Column("time", Time))
             ]

class TestType_Schedual(Tree):
    master = TestType
    name = "schedual"
    tables = [
                TableModel("schedual", Column("begintime", Time), Column("endtime", Time),
                                       Column("task", String), Column("day", Date))
             ]



Tree.handle_branches()

#TableModel(tablename="timeperday", inheritance=InheritRowToCol(parent=TestType, tablename="tasks", column="task"),
#                           coltype_inheritance=Integer,
#                           day=Date),
