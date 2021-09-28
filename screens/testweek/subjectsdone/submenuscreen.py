from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timecounter import TimeCounter
from plannings.time.timedicts import *
from screens.testweek.subjectsdone.dialogcontent import DialogContent_TestWeek_SubjectsDone
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
import globals


class SubjectDoneItem(OneLineAvatarIconListItem):
    def __init__(self, master, subjectr, time, **kwargs):
        self.master = master
        self.subjectr = subjectr
        self.time = time
        super().__init__(**kwargs)

    def get_color(self):
        return "#000000"

    def open_details(self):
        globals.sm.show_screen(screen=self.master.branch.screens["details"](self.master.applr, self.subjectr))

class SubMenuScreen_TestWeek_SubjectsDone(DynamicScreen):
    dialogadd = None
    def __init__(self, applr, **kwargs):
        self.screenname = "submenuscreen_testweek_subjectsdone"
        self.applr = applr
        super().__init__(**kwargs)
        self.handle_data()
        self.count_time()
        for subjectr in self.subjectlist: # assigned in self.handle_data()
            donetime = self.donedict[subjectr["subject"]]
            self.ids.subjects.add_widget(SubjectDoneItem(self, subjectr, donetime))

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, applid=self.applr.id) # a TableCollection object with access to table objects
        self.subjecttable = self.branch.master.load(globals.d, applid=self.applr.id)["subjects"]; self.subjectlist = self.subjecttable.data
        self.table = self.tablecoll["subjectsdone"]
        self.data_use = [self.table, self.subjecttable]
        self.data = self.table.data

    def count_time(self):
        self.donedict = {}
        for subjectr in self.subjectlist:
            subject = subjectr["subject"]
            time = TimeCounter(0,0)
            for row in self.data: # var "row" in form (subject, donetime, date)
                if not subject == row["subject"]: continue # only continue if the subject is right
                t = eval(row["donetime"]) # in form tuple(hour, time)
                time.add_time(*t)
            self.donedict[subject] = time

    def add_time_gui(self, subjectr):
        subject = subjectr.subject
        self.dialogadd = MDDialog(title=subject, type="custom", buttons=[
                    MDFlatButton(text="CANCEL", on_release=lambda _: self.dialogadd.dismiss()),
                    MDFlatButton(text="SAVE", on_release=lambda _: self.save()),],
                    content_cls=DialogContent_TestWeek_SubjectsDone(subjectr)
                    )
        self.dialogadd.open()

    def save(self):
        data = self.dialogadd.content_cls.collectdata() # ex: {"subject": maths, "donetime": "(1,22)", "date": datetime.date(2003,5,8)} (or None when invalidation)
        if not data: # some textfield is not filled with a positive integer
            Snackbar(text="invalid hours or minutes", duration=1).open()
            return 0
        self.table.add_row(**data)
        self.dialogadd.dismiss()
