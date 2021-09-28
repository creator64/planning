from plannings.screens.dynamic_screen import DynamicScreen
from plannings.database.where import WHERE, eq
from plannings.time.timedicts import *
from plannings.time.timestrings import *
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
import globals


class SubjectDetailItem(OneLineAvatarIconListItem):
    def __init__(self, master, subjectr, **kwargs):
        self.master = master
        self.subjectr = subjectr
        super().__init__()

    def get_text(self):
        date = self.subjectr["date"]; donetime = eval(self.subjectr["donetime"])
        text = f"{timestr_with_weekday(date)}: {donetime[0]}h {donetime[1]}m"
        return text

class Details_TestWeek_SubjectsDone(DynamicScreen):
    deldialog = None
    def __init__(self, applr, subjectr, **kwargs):
        self.screenname = "details_testweek_subjectsdone"
        self.applr = applr
        self.subjectr = subjectr
        self.required_args = ["applr.id", "subjectr.subject"]
        super().__init__(self.required_args, **kwargs)
        self.handle_data()
        for record in self.data: # record in form: (subject, donetime, date)
            self.ids.subjectdetails.add_widget(SubjectDetailItem(self, record))

    def handle_data(self):
        wh = {"subjectsdone": WHERE(subject=eq(self.subjectr.subject))}
        self.tablecoll = self.branch.load(globals.d, applid=self.applr.id,\
                         WHERE=wh, ORDER_BY={"subjectsdone": ("date",)}) # a TableCollection object with access to table objects
        self.table = self.tablecoll["subjectsdone"]
        self.data_use = [self.table]
        self.data = self.table.data

    def delete_gui(self, subjectitem):
        self.deldialog = MDDialog(title="delete", text=f"weet je zeker dat je wil verwijderen?", buttons=[
                MDRaisedButton(text="CANCEL", on_release=lambda _: self.deldialog.dismiss()),
                MDRaisedButton(text="DELETE", on_release=lambda _: self.delete(subjectitem))])
        self.deldialog.open()

    def delete(self, subjectitem):
        subjectr = subjectitem.subjectr
        wh = WHERE(id=eq(subjectr.id))
        self.table.delete_row(WHERE=wh)
        self.deldialog.dismiss()
