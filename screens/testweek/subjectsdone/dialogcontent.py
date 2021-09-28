from plannings.time.timedicts import *
from plannings.time.timecounter import TimeCounter
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.picker import MDDatePicker
from datetime import date

class DialogContent_TestWeek_SubjectsDone(BoxLayout):
    def __init__(self, subjectr, **kwargs):
        self.subjectr = subjectr
        self.currentdate = date.today()
        super().__init__(**kwargs)

    def validate(self):
        if self.ids.hours.text.isdigit(): # check if hours textfield is filled with an integer
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
        print("hu")
        self.currentdate = date
        self.ids.date.text = self.get_date_str()

    def collectdata(self):
        if not self.validate(): return None
        date = self.currentdate
        subject = self.subjectr.subject
        t = TimeCounter(hours=int(self.ids.hours.text), minutes=int(self.ids.minutes.text)) # timecounter will handle it if adding for ex 80 minutes
        time = (t.hours, t.minutes)
        return {"subject": subject, "donetime": str(time), "date": date}
