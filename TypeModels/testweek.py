from plannings.modeling.tree import Tree
from plannings.modeling.tablemodel import TableModel
from sqlalchemy import Integer, String, Boolean, Date, Time, DateTime, Float, Column
from screens.testweek.menuscreen import MenuScreen_TestWeek
from screens.testweek.submenuscreen import SubMenuScreen_TestWeek
from screens.testweek.addsubject import AddSubject_TestWeek
from screens.testweek.subjectsdone.submenuscreen import SubMenuScreen_TestWeek_SubjectsDone
from screens.testweek.subjectsdone.details import Details_TestWeek_SubjectsDone
from screens.testweek.subjectcommentarydays.submenuscreen import SubMenuScreen_TestWeek_SubjectCommentaryDays
from screens.testweek.subjectcommentarydays.overview import Overview_Day_TestWeek_SubjectCommentaryDays, Overview_Subject_TestWeek_SubjectCommentaryDays
from screens.testweek.subjectcommentarydays.details import Details_TestWeek_SubjectCommentaryDays
from screens.testweek.dayplanning.submenuscreen import SubMenuScreen_TestWeek_DayPlanning
from screens.testweek.dayplanning.overview import Overview_TestWeek_DayPlanning
from screens.testweek.subjectpartvalue.submenuscreen import SubMenuScreen_TestWeek_SubjectPartValue

class TestWeek(Tree):
    name = "Test Week"
    istype = True
    tables = [
        TableModel("subjects", Column("subject", String), Column("mark", Float), Column("testdate", Date),
                               Column("time", Time), Column("learningcontent", String))
    ]
    menuscreen = MenuScreen_TestWeek
    submenuscreen = SubMenuScreen_TestWeek
    screens = {"submenuscreen": SubMenuScreen_TestWeek, "addsubject": AddSubject_TestWeek}

class TestWeek_DayPlanning(Tree):
    master = TestWeek
    name = "Day planning"
    tables = [
        TableModel("dayplanning", Column("id", Integer, primary_key=True), Column("subject", String),
                                  Column("begintime", Time), Column("endtime", Time),
                                  Column("date", Date), Column("done", Boolean)),
        TableModel("days", Column("day", Date))
    ]
    screens = {"submenuscreen": SubMenuScreen_TestWeek_DayPlanning, "overview": Overview_TestWeek_DayPlanning}

class TestWeek_SubjectCommentaryDays(Tree):
    master = TestWeek
    name = "Subjectcommentarydays"
    tables = [
        TableModel("subjectcommentarydays", Column("subject", String), Column("comment", String),
                                            Column("date", Date)),
        TableModel("days", Column("day", Date))
    ]
    screens = {"submenuscreen": SubMenuScreen_TestWeek_SubjectCommentaryDays,
               "overviewday": Overview_Day_TestWeek_SubjectCommentaryDays,
               "overviewsubject": Overview_Subject_TestWeek_SubjectCommentaryDays,
               "details": Details_TestWeek_SubjectCommentaryDays}

class TestWeek_SubjectPartValue(Tree):
    master = TestWeek
    name = "Subjectpartvalue"
    tables = [
        TableModel("subjectpartvalue", Column("subject", String), Column("part", String), Column("value", Integer)),
        TableModel("parts", Column("part", String))
    ]
    screens = {"submenuscreen": SubMenuScreen_TestWeek_SubjectPartValue}

class TestWeek_SubjectsDone(Tree):
    master = TestWeek
    name = "Subjects done"
    tables = [
        TableModel("subjectsdone", Column("id", Integer, primary_key=True), Column("subject", String),
                                   Column("donetime", String, server_default="(0,0)"), Column("date", Date))
    ]
    screens = {"submenuscreen": SubMenuScreen_TestWeek_SubjectsDone,
               "details": Details_TestWeek_SubjectsDone}

Tree.handle_branches()
