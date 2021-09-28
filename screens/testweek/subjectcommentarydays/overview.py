from plannings.screens.dynamic_screen import DynamicScreen
from plannings.database.where import WHERE, eq
from plannings.time.timestrings import *
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import globals


class Scd_Overview_Subject(TwoLineAvatarIconListItem):
    def __init__(self, subject, content, **kwargs):
        self.subject = subject
        self.content = content
        super().__init__(**kwargs)

class Scd_Overview_Day(TwoLineAvatarIconListItem):
    def __init__(self, day, content, **kwargs):
        self.day = day
        self.content = content
        self.day_str = timestr_with_weekday(self.day)
        super().__init__(**kwargs)

class Overview_Subject_TestWeek_SubjectCommentaryDays(DynamicScreen):
    def __init__(self, applr, subjectr, **kwargs):
        self.applr = applr
        self.subjectr = subjectr
        self.required_args = ["applr.id", "subjectr.subject"]
        self.screenname = "overview_subject_testweek_subjectcommentarydays"
        super().__init__(self.required_args, **kwargs)
        self.handle_data()
        for record in self.table: # (subject, comment, date)
            subject, comment, date = record
            self.ids.list.add_widget(Scd_Overview_Day(date, comment))
        items = [
                {"viewclass": "OneLineListItem",
                "text": subjectr.subject, "height": dp(56),
                "on_release": lambda x=subjectr: self.show_subject(x)}
                for subjectr in self.subjectlist if subjectr.subject != self.subjectr.subject # go through subjectlist and add items to menuscreen (not the subject were already at)
                ]
        self.subjectswitch = MDDropdownMenu(items=items, width_mult=4)

    def show_subjectswitch(self, caller):
        self.subjectswitch.caller = caller
        self.subjectswitch.open()

    def show_subject(self, subjectr):
        self.subjectswitch.dismiss()
        sc = self.branch.screens["overviewsubject"]
        globals.sm.show_screen(screen=sc(self.applr, subjectr))

    def handle_data(self):
        """We want 3 tables: the daytable, the subjecttable and the subjectplanningdays table (see DB Browser for columns and info)"""
        ob = {"days": ("day",), "subjectcommentarydays": ("date",)}
        wh = {"subjectcommentarydays": WHERE(subject=eq(self.subjectr.subject))} # when were in a math overview we only care about records with subject=math
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY=ob, WHERE=wh) # a TableCollection object with access to table objects
        self.tablecollmaster = self.branch.master.load(globals.d, self.applr.id, ORDER_BY={"subjects": ("testdate", "time")})
        self.data_use = [self.tablecoll["days"], self.tablecoll["subjectcommentarydays"], self.tablecollmaster["subjects"]]
        self.daylist = self.data_use[0].data; self.subjectlist = self.data_use[2].data;
        self.table = self.data_use[1].data # (subject, comment, date)

    def show_editscreen(self, _):
        sc = self.branch.screens["details"]
        globals.sm.show_screen(screen=sc(self.applr))

class Overview_Day_TestWeek_SubjectCommentaryDays(DynamicScreen):
    def __init__(self, applr, day, **kwargs):
        self.applr = applr
        self.day = day
        self.required_args = ["applr.id", "day"]
        self.screenname = "overview_day_testweek_subjectcommentarydays"
        self.day_str = timestr_with_weekday(self.day)
        super().__init__(self.required_args, **kwargs)
        self.handle_data()
        for record in self.table: # (subject, comment, date)
            subject, comment, date = record
            self.ids.list.add_widget(Scd_Overview_Subject(subject, comment))
        items = [
                {"viewclass": "OneLineListItem",
                "text": timestr_with_weekday(day.day), "height": dp(56),
                "on_release": lambda x=day.day: self.show_day(x)}
                for day in self.daylist if day.day != self.day # go through daylist and add items to menuscreen (not the day were already at)
                ]
        self.dayswitch = MDDropdownMenu(items=items, width_mult=4)

    def show_dayswitch(self, caller):
        self.dayswitch.caller = caller
        self.dayswitch.open()

    def show_day(self, day):
        self.dayswitch.dismiss()
        sc = self.branch.screens["overviewday"]
        globals.sm.show_screen(screen=sc(self.applr, day))

    def handle_data(self):
        """We want 3 tables: the daytable, the subjecttable and the subjectplanningdays table (see DB Browser for columns and info)"""
        ob = {"days": ("day",)}
        wh = {"subjectcommentarydays": WHERE(date=eq(self.day))} # get only the records where day=the day of this overview
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY=ob, WHERE=wh) # a TableCollection object with access to table objects
        self.tablecollmaster = self.branch.master.load(globals.d, self.applr.id, ORDER_BY={"subjects": ("testdate", "time")})
        self.data_use = [self.tablecoll["days"], self.tablecoll["subjectcommentarydays"], self.tablecollmaster["subjects"]]
        self.daylist = self.data_use[0].data; self.subjectlist = self.data_use[2].data;
        self.table = self.data_use[1].data # (subject, comment, date)

    def show_editscreen(self, _):
        sc = self.branch.screens["details"]
        globals.sm.show_screen(screen=sc(self.applr))
