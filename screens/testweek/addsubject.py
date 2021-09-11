from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen
from plannings.database.where import WHERE, eq
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.snackbar import Snackbar
from datetime import date as d, time as t, datetime as dt
import globals

class AddSubject_TestWeek(DynamicScreen):
    delete_on_leave = True
    def __init__(self, applr, subjectr=None, **kwargs):
        self.applr = applr
        self.screenname = "addsubject_testweek"
        self.subjectr = subjectr # if adding a new subject its set to None otherwise its set to a row object of sqlalchemy
        self.temp_date = d.today()
        if self.subjectr: self.temp_date = self.subjectr.testdate
        super().__init__(**kwargs)
        self.ids.nomark.bind(active=self.on_nomark_hit)
        self.handle_data()

    def on_nomark_hit(self, cb, state):
        if state == True:
            self.ids.mark.text = ""
            self.ids.mark.readonly = True
        else:
            self.ids.mark.readonly = False

    def handle_data(self):
        self.ids.date.text = self.print_date(self.temp_date)
        if not self.subjectr: return None # means were adding a new subject and we dont have to fill in the gui (except for the date)
        self.ids.subject.text = self.subjectr.subject
        if self.subjectr.mark:
            self.ids.mark.text = str(self.subjectr.mark)
        else:
            self.ids.nomark.active = True
            self.ids.mark.readonly = True
        self.ids.learningcontent.text = self.subjectr.learningcontent
        if self.subjectr.time:
            self.ids.time.text = str(self.subjectr.time.hour) + ":" + str(self.subjectr.time.minute)
            if self.subjectr.time.minute == 0:
                self.ids.time.text += "0"

    def change_date(self):
        date_dialog = MDDatePicker(day=self.temp_date.day, month=self.temp_date.month, year=self.temp_date.year)
        date_dialog.bind(on_save=lambda _, date, _2: self.save_date(date))
        date_dialog.open()

    @staticmethod
    def print_date(date):
        MonthDict = {1: "januari", 2: "februari", 3: "maart", 4: "april", 5: "mei", 6: "juni", 7: "juli", \
                     8: "augustus", 9: "september", 10: "okobert", 11: "november", 12: "december"}
        DayDict = {0: "maandag", 1: "dinsdag", 2: "woensdag", 3: "donderdag", 4: "vrijdag", 5: "zaterdag", 6: "zondag"}
        return f"{DayDict[date.weekday()]} {date.day} {MonthDict[date.month]}"

    def save_date(self, date):
        self.temp_date = date
        self.ids.date.text = self.print_date(date)

    def subject_check(self):
        if self.ids.subject.text: return True
        return False

    def mark_check(self):
        mark = self.ids.mark.text
        if self.ids.nomark.active:
            return True
        try:
            validmark = float(mark)
            if validmark <= 10 and validmark >=1 and str(validmark)[::-1].find('.') <= 1: # third condition is amount of decimals, see: https://stackoverflow.com/questions/26231755/count-decimal-places-in-a-float
                return True
            return False
        except ValueError: return False

    def time_check(self):
        time = self.ids.time.text
        timeformat = "%H:%M"
        if time == "":
            return True
        try:
            validtime = dt.strptime(time, timeformat)
            return True
        except ValueError:
            return False

    def validation_check(f):
        def wrapper(self, *args, **kwargs):
            if self.subject_check() and self.mark_check() and self.time_check():
                print("everythings fine")
                r = f(self, *args, **kwargs)
                return r
            else:
                Snackbar(text="Niet correct ingevuld", duration=1).open()
        return wrapper

    @validation_check
    def save(self):
        if self.subjectr: self.update_subject()
        else: self.add_subject()

    def collectdata(self):
        data = {}
        data["subject"] = self.ids.subject.text
        if self.ids.nomark.active:
            data["mark"] = None
        else: data["mark"] = float(self.ids.mark.text)
        data["learningcontent"] = self.ids.learningcontent.text
        data["testdate"] = d(year=self.temp_date.year, month=self.temp_date.month, day=self.temp_date.day)
        if timestr := self.ids.time.text:
            tl = timestr.split(":")
            data["time"] = t(hour=int(tl[0]), minute=int(tl[1]))
        else: data["time"] = None
        return data

    def add_subject(self):
        subjecttable = self.branch.load(globals.d, applid=self.applr.id)["subjects"]
        data = self.collectdata()
        subjecttable.add_row(**data)
        globals.sm.show_screen(screen=self.branch.screens["submenuscreen"](self.applr))

    def update_subject(self):
        subjecttable = self.branch.load(globals.d, applid=self.applr.id)["subjects"]
        data = self.collectdata()
        wh = WHERE(subject=eq(self.subjectr.subject))
        subjecttable.update(**data, WHERE=wh)
        globals.sm.show_screen(screen=self.branch.screens["submenuscreen"](self.applr))
