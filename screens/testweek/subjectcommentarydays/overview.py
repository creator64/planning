from plannings.screens.dynamic_screen import DynamicScreen
from plannings.database.where import WHERE, eq
from plannings.time.timestrings import *
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.metrics import dp
import globals


class Scd_Overview_Subject(TwoLineAvatarIconListItem):
    def __init__(self, master, subject, content, go_to_edit=True, **kwargs):
        self.subject = subject
        self.content = content
        self.master = master
        self.go_to_edit = go_to_edit
        super().__init__(**kwargs)

    def on_release(self):
        if not self.go_to_edit: return # if we have chosen that we dont wanna go to the edit page on click, we stop the function
        sc = self.master.branch.screens["details"]
        globals.sm.show_screen(screen=sc(self.master.applr))
        details_sc = globals.sm.get_screen(globals.sm.current) # getting the actual screen instance that is showing up. See structure of sm.show_screen
        details_sc.change(subject=self.subject, day=self.master.day)

class Scd_Overview_Day(TwoLineAvatarIconListItem):
    def __init__(self, master, day, content, go_to_edit=True, **kwargs):
        self.day = day
        self.content = content
        self.day_str = timestr_with_weekday(self.day)
        self.master = master
        self.go_to_edit = go_to_edit
        super().__init__(**kwargs)

    def on_release(self):
        if not self.go_to_edit: return # see Scd_Overview_Subject
        sc = self.master.branch.screens["details"]
        globals.sm.show_screen(screen=sc(self.master.applr))
        details_sc = globals.sm.get_screen(globals.sm.current) # getting the actual screen instance that is showing up. See structure of sm.show_screen
        details_sc.change(day=self.day, subject=self.master.subjectr.subject)

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
            self.ids.list.add_widget(Scd_Overview_Day(self, date, comment))
        self.handle_subjectswitch()
        self.check_test_dates()

    def handle_subjectswitch(self):
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

    def check_test_dates(self):
        date = self.subjectr.testdate
        comment = "[b]Proefwerk"
        self.ids.list.add_widget(Scd_Overview_Day(self, date, comment, go_to_edit=False))

class Overview_Day_TestWeek_SubjectCommentaryDays(DynamicScreen):
    deldialog = None
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
            self.ids.list.add_widget(Scd_Overview_Subject(self, subject, comment))
        self.handle_day_switch()
        self.check_test_dates()

    def handle_day_switch(self):
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

    def delete_gui(self, _):
        if not self.deldialog:
            self.deldialog = MDDialog(
                text="Do you really want to delete this day?",
                buttons=[
                    MDFlatButton(text="CANCEL", on_release=lambda _: self.deldialog.dismiss()),
                    MDFlatButton(text="DELETE", text_color=(1,0,0,1), theme_text_color="Custom", on_release=lambda _: self.delete())])
        self.deldialog.open()

    def delete(self):
        self.deldialog.dismiss()
        # 1. switch to the right screen
        # 2. remove this screen before any db changes are made
        # 3. delete the day from the daytable
        # 4. delete all records with this day from the main table
        sc = self.branch.screens["submenuscreen"] # 1
        self.manager.show_screen(screen=sc(self.applr)) # 1
        self.manager.remove_widget(self) # 2
        daytable = self.data_use[0]; maintable = self.data_use[1] # 3; 4
        wh = WHERE(day=eq(self.day)) # 3
        daytable.delete_row(WHERE=wh) # 3
        wh = WHERE(date=eq(self.day)) # 4
        maintable.delete_row(WHERE=wh) # 4

    def check_test_dates(self):
        for subjectr in self.subjectlist:
            if subjectr.testdate == self.day:
                subject = subjectr.subject
                comment = "[b]Proefwerk"
                self.ids.list.add_widget(Scd_Overview_Subject(self, subject, comment, go_to_edit=False))
