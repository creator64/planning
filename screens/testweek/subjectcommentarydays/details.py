from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timestrings import *
from plannings.database.where import WHERE, eq
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import globals

class Details_TestWeek_SubjectCommentaryDays(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "details_testweek_subjectcommentarydays"
        self.currentsubject = None; self.currentday = None
        self.tempsaves = []
        super().__init__(**kwargs)
        self.handle_data()
        subjectmenuitems = [
            {"viewclass": "OneLineListItem",
            "text": subjectr.subject, "height": dp(56),
            "on_release": lambda x=subjectr.subject: self.change(subject=x)}
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
        self.change(subject=self.subjectlist[0].subject, day=self.daylist[0].day)

    def handle_data(self):
        """We want 3 tables: the daytable, the subjecttable and the subjectplanningdays table (see DB Browser for columns and info)"""
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY={"days": ("day",)}) # a TableCollection object with access to table objects
        self.tablecollmaster = self.branch.master.load(globals.d, self.applr.id, ORDER_BY={"subjects": ("testdate", "time")})

        self.data_use = [self.tablecoll["days"], self.tablecoll["subjectcommentarydays"], self.tablecollmaster["subjects"]]
        self.daytable, self.maintable, self.subjecttable = self.data_use

        self.daylist = self.daytable.data; self.subjectlist = self.subjecttable.data;
        self.maindata = self.maintable.data # (subject, comment, date)

    def get_temp_record(self):
        try:
            record = list(filter(lambda r: r["subject"]==self.currentsubject and r["date"]==self.currentday, self.tempsaves))[0]
            return record
        except IndexError: return None

    def get_record(self):
        try:
            record = list(filter(lambda r: r.subject==self.currentsubject and r.date==self.currentday, self.maindata))[0]
            return record
        except IndexError: return None

    def change(self, subject=None, day=None):
        self.save_temp()
        if not subject and not day:
            raise Exception("at least one param should be filled")
        elif not subject: subject = self.currentsubject
        elif not day: day = self.currentday
        self.currentsubject = subject; self.currentday = day
        record = self.get_temp_record() # if theres a temp record fill it with this one
        if not record:
            record = self.get_record() # if not fill with whats stored in db
        self.ids.subjectmenubutton.text = subject
        self.ids.daymenubutton.text= str(day)
        self.fill(record)
        self.subjectmenu.dismiss(); self.daymenu.dismiss()

    def fill(self, record):
        if not record:
            self.ids.content.text = ""
            return 0
        self.ids.content.text = record["comment"]
        return 1

    def show_menu(self, type):
        if type == "subject": self.subjectmenu.open()
        elif type == "day": self.daymenu.open()

    def save_temp(self):
        content = self.ids.content.text # what we filled in the moment were about to change from subject or day
        record = self.get_record() # a tup (subj, comment, date) stored in the db
        tr = self.get_temp_record() # same as record but maybe weve already edited sth
        if tr:
            if content == tr["comment"]: return # nth changed
        elif record: # check if theres a record in the db of the current subject and day
            if content == record["comment"]: return # nth changed
        elif not content: return # no current record: if no content then nth changed too and the func can stop
        if tr:
            self.tempsaves.remove(tr) # delete the temp_record thats already in the temp_saves
        if not content:
            self.tempsaves.append({"type": "delete", "subject": self.currentsubject, "date": self.currentday})
        elif not record:
            self.tempsaves.append({"type": "add", "subject": self.currentsubject, "date": self.currentday, "comment": content})
        else:
            self.tempsaves.append({"type": "update", "subject": self.currentsubject, "date": self.currentday, "comment": content})
        print(self.tempsaves)

    def save(self):
        self.save_temp()
        for n, tr in enumerate(self.tempsaves):
            us = False
            if n == len(self.tempsaves) - 1: us = True # preventing to update all the screens every time we update a change
            if tr["type"] == "add":
                self.maintable.add_row(subject=tr["subject"], date=tr["date"], comment=tr["comment"], update_screens=us)
            elif tr["type"] == "update":
                wh = WHERE(subject=eq(tr["subject"]), date=eq(tr["date"]))
                self.maintable.update(WHERE=wh, comment=tr["comment"], update_screens=us)
            elif tr["type"] == "delete":
                wh = WHERE(subject=eq(tr["subject"]), date=eq(tr["date"]))
                self.maintable.delete_row(WHERE=wh, update_screens=us)
