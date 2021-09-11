from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timecounter import TimeCounter
from kivymd.uix.list import OneLineListItem
import globals


class SubjectDoneItem(OneLineListItem):
    def __init__(self, subjectr, time, **kwargs):
        self.subjectr = subjectr
        self.time = time
        super().__init__(**kwargs)

class SubMenuScreen_TestWeek_SubjectsDone(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.screenname = "submenuscreen_testweek_subjectsdone"
        self.applr = applr
        super().__init__(**kwargs)
        self.handle_data()
        self.count_time()
        for subjectr in self.subjectlist: # assigned in self.handle_data()
            donetime = self.donedict[subjectr["subject"]]
            self.ids.subjects.add_widget(SubjectDoneItem(subjectr, donetime))

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
