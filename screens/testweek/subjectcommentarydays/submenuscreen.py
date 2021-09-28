from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timestrings import *
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.picker import MDDatePicker
from kivy.uix.scrollview import ScrollView
import globals


class Scd_SubjectItem(OneLineListItem):
    def __init__(self, master, subjectr, **kwargs):
        self.master = master
        self.subjectr = subjectr
        super().__init__(**kwargs)

    def show_overview(self):
        screen = self.master.master.branch.screens["overviewsubject"]
        globals.sm.show_screen(screen=screen(self.master.master.applr, self.subjectr))

class Scd_DayItem(OneLineListItem):
    def __init__(self, master, day, **kwargs):
        self.master = master
        self.day = day
        super().__init__(**kwargs)

    def get_day_str(self):
        return timestr_with_weekday(self.day)

    def show_overview(self):
        screen = self.master.master.branch.screens["overviewday"]
        globals.sm.show_screen(screen=screen(self.master.master.applr, self.day))

class TabSubjects(ScrollView, MDTabsBase):
    '''Class implementing content for a tab.'''
    def __init__(self, master, data, **kwargs):
        self.master = master
        self.data = data
        super().__init__(**kwargs)
        for subjectr in self.data: # record in form for ex: (WisB, 10, DateOfTest, more_data)
            self.ids.list.add_widget(Scd_SubjectItem(self, subjectr))

class TabDays(ScrollView, MDTabsBase):
    '''Class implementing content for a tab.'''
    def __init__(self, master, data, **kwargs):
        self.master = master
        self.data = data
        super().__init__(**kwargs)
        for record in self.data: # record in form (DateTime.Date Object(y,m,d),)
            self.ids.list.add_widget(Scd_DayItem(self, record.day))

class SubMenuScreen_TestWeek_SubjectCommentaryDays(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek_subjectcommentarydays"
        super().__init__(**kwargs)
        self.handle_data()
        self.ids.tabs.add_widget(TabDays(self, self.daylist))
        self.ids.tabs.add_widget(TabSubjects(self, self.subjectlist))

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY={"days": ("day",)}) # a TableCollection object with access to table objects
        self.tablecollmaster = self.branch.master.load(globals.d, self.applr.id, ORDER_BY={"subjects": ("testdate", "time")})
        self.data_use = [self.tablecoll["days"], self.tablecollmaster["subjects"]]
        self.daylist = self.data_use[0].data; self.subjectlist = self.data_use[1].data

    def newday(self):
        dp = MDDatePicker()
        dp.bind(on_save=lambda dp, date, _: self.save(date))
        dp.open()

    def save(self, date):
        daytable = self.tablecoll["days"]
        if daytable.check_value_exist_in_col(col="day", value=date):
            Snackbar(text="Dag bestaat al", duration=1).open()
        else:
            daytable.add_row(day=date)
