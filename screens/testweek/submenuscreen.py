from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen
from plannings.database.where import WHERE, eq
from plannings.time.timedicts import *
from TypeModels.testweek.vars import get_sub_im, get_mark_color
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarIconListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from datetime import date as d
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.snackbar import Snackbar
import globals


class SubjectItem(ThreeLineAvatarIconListItem):
    dialog = None
    def __init__(self, master, subjectr, **kwargs):
        self.master = master
        self.subjectr = subjectr
        super().__init__(**kwargs)

    def get_text(self):
        text = self.subjectr.subject
        if self.subjectr.mark:
            text += ": " + str(self.subjectr.mark)
        return f"[color={self.get_color()}]" + text + "[/color]"

    def print_date_time(self):
        wd = self.subjectr.testdate.weekday()
        text = f"{DayDict[wd]} {self.subjectr.testdate.day} {MonthDict[self.subjectr.testdate.month]} "
        if t := self.subjectr.time:
            text += str(t.hour) + ":" + str(t.minute)
            if t.minute == 0:
                text += "0"
        return text

    def get_image(self):
        return get_sub_im(self.subjectr.subject)

    def get_color(self):
        return get_mark_color(self.subjectr.mark)

    def delete_gui(self, icon):
        self.dialog = MDDialog(text="Are you sure you want to delete %s from your subjects?" %(self.subjectr.subject),
                 buttons=[MDFlatButton(text="CANCEL", on_release=lambda x: self.dialog.dismiss()),
                          MDFlatButton(text="DELETE", on_release=lambda x: self.master.delete(self))])
        self.dialog.open()

class SubMenuScreen_TestWeek(DynamicScreen):
    dialog = None
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek"
        super().__init__(**kwargs)
        self.handle_data()
        for subject in self.data:
            self.ids.subjectlist.add_widget(SubjectItem(self, subject))

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, applid=self.applr.id, ORDER_BY={"subjects": ("testdate", "time")}) # a TableCollection object with access to table objects
        self.data_use = [self.tablecoll["subjects"]] # specify the tables we use for the update system
        self.data = self.data_use[0].data # get data of subjects applications

    def new(self):
        globals.sm.show_screen(screen=self.branch.screens["addsubject"](self.applr))

    def delete(self, subjectitem):
        subjecttable = self.data_use[0]
        wh = WHERE(subject=eq(subjectitem.subjectr.subject))
        subjecttable.delete_row(WHERE=wh)
        subjectitem.dialog.dismiss()
        Snackbar(text="Subject removed successfully", duration=1).open()

    def edit_subject(self, subjectitem):
        globals.sm.show_screen(screen=self.branch.screens["addsubject"](self.applr, subjectr=subjectitem.subjectr))
