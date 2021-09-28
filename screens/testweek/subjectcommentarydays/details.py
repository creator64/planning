from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timestrings import *
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import globals

class Details_TestWeek_SubjectCommentaryDays(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "details_testweek_subjectcommentarydays"
        super().__init__(**kwargs)
        self.handle_data()
        subjectmenuitems = [
            {"viewclass": "OneLineListItem",
            "text": subjectr.subject, "height": dp(56),
            "on_release": lambda x=subjectr: self.change(subjectr=x)}
            for subjectr in self.subjectlist
        ]
        daymenuitems = [
                {"viewclass": "OneLineListItem",
                "text": timestr_with_weekday(day.day), "height": dp(56),
                "on_release": lambda x=day.day: self.change(day=x)}
                for day in self.daylist # go through daylist and add items to menuscreen (not the day were already at)
                ]
        self.subjectmenu = MDDropdownMenu(items=subjectmenuitems, width_mult=4, caller=self.ids.subjectmenubutton)
        self.daymenu = MDDropdownMenu(items=daymenuitems, width_mult=4, caller=self.ids.daymenubutton)

    def handle_data(self):
        """We want 3 tables: the daytable, the subjecttable and the subjectplanningdays table (see DB Browser for columns and info)"""
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY={"days": ("day",)}) # a TableCollection object with access to table objects
        self.tablecollmaster = self.branch.master.load(globals.d, self.applr.id, ORDER_BY={"subjects": ("testdate", "time")})

        self.data_use = [self.tablecoll["days"], self.tablecoll["subjectcommentarydays"], self.tablecollmaster["subjects"]]
        self.daytable, self.maintable, self.subjecttable = self.data_use

        self.daylist = self.daytable.data; self.subjectlist = self.subjecttable.data;
        self.maindata = self.maintable.data # (subject, comment, date)

    def change(self, subjectr=None, day=None):
        pass

    def show_menu(self, type):
        if type == "subject": self.subjectmenu.open()
        elif type == "day": self.daymenu.open()
