from plannings.time.timedicts import *
from plannings.time.timecounter import TimeCounter
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from datetime import date

class DialogContent_TestWeek_SubjectsDone(BoxLayout):
    def __init__(self, subjectr, **kwargs):
        self.subjectr = subjectr
        self.currentdate = date.today()
        self.allrecords = [] # a list of all the records for ex [{"subject": "NL", "time": "(1,30)", "date": "some date"}, {"subject": "NL", "time": "(3,30)", "date": "some other date"}
        super().__init__(**kwargs)

    def validate(self):
        if self.ids.hours.text.isdigit() or self.ids.hours.text == "": # check if hours textfield is filled with an integer
            return True
        else: return False
        if self.ids.minutes.text.isdigit(): # check if minutes textfield is filled with an integer
            return True
        else: return False

    def get_date_str(self):
        d = self.currentdate
        return f"{d.day}-{d.month}-{d.year}"

    def change_date(self):
        d = self.currentdate
        dp = MDDatePicker(year=d.year, month=d.month, day=d.day)
        dp.bind(on_save=self.save_current_date)
        dp.open()

    def save_current_date(self, _, date, __):
        self.currentdate = date
        self.ids.date.text = self.get_date_str()

    def addrecord(self):
        data = self.collectdata()
        if not data: # some textfield is not filled with a positive integer
            Snackbar(text="invalid hours or minutes", duration=1).open()
            return 0
        time = eval(data["donetime"]) # a tuple (hours, minutes)
        self.ids.recordlist.add_widget(MDLabel(text="op " + str(data["date"]) + " " + str(time[0]) + " uur en " + str(time[1]) + " minuten gewerkt", height=20))
        self.allrecords.append(data)

    def collectdata(self):
        if not self.validate(): return None
        date = self.currentdate
        subject = self.subjectr.subject
        hours = self.ids.hours.text; minutes = self.ids.minutes.text
        if hours == "": hours = 0
        if minutes == "": minutes = 0
        t = TimeCounter(hours=int(hours), minutes=int(minutes)) # timecounter will handle it if adding for ex 80 minutes
        time = (t.hours, t.minutes)
        return {"subject": subject, "donetime": str(time), "date": date}
