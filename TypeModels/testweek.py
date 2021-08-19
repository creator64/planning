from plannings.modeling.tree import Tree
from plannings.modeling.tablemodel import TableModel
from sqlalchemy import Integer, String, Boolean, Date, Time, DateTime, Column
from screens.testweek.createscreen import CreateScreen_TestWeek

class TestWeek(Tree):
    name = "Test Week"
    istype = True
    tables = [
        TableModel("subjects", Column("subject", String), Column("mark", Integer), Column("testdate", DateTime),
                               Column("learningcontent", String))
    ]
    createscreen = CreateScreen_TestWeek

class TestWeek_DayPlanning(Tree):
    master = TestWeek
    name = "Day planning"
    tables = [
        TableModel("dayplanning", Column("subject", String), Column("begintime", Time), Column("endtime", Time),
                                  Column("date", Date))
    ]

class TestWeek_SubjectCommentaryDays(Tree):
    master = TestWeek
    name = "Subjectcommentary days"
    tables = [
        TableModel("subjectcommentarydays", Column("subject", String), Column("comment", String), Column("date", Date))
    ]

class TestWeek_SubjectPartValue(Tree):
    master = TestWeek
    name = "Subjectpartvalue"
    tables = [
        TableModel("subjectpartvalue", Column("subject", String), Column("part", String), Column("value", Integer))
    ]

class TestWeek_SubjectsDone(Tree):
    master = TestWeek
    name = "Subjects done"
    tables = [
        TableModel("subjectsdone", Column("subject", String), Column("donetime", Time), Column("date", Date))
    ]
