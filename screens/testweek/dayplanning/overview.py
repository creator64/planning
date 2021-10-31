from plannings.screens.dynamic_screen import DynamicScreen
from plannings.database.where import WHERE, eq
from plannings.time.timestrings import *
from screens.testweek.dayplanning.dialogcontent import DP_Overview_DialogContent
from copy import copy
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
import globals


class DP_ToDoItem(OneLineAvatarIconListItem):
    def __init__(self, master, todor, **kwargs):
        self.master = master
        self.todor = todor
        super().__init__(**kwargs)

    def on_release(self):
        self.master.dialog = MDDialog(
            title="Plan een vak",
            type="custom",
            content_cls=DP_Overview_DialogContent(self.master, todor=self.todor),
            buttons=[MDFlatButton(text="CANCEL", on_release=lambda _: self.master.dialog.dismiss()),
                     MDFlatButton(text="DELETE", text_color=(1,0,0,1), theme_text_color="Custom", \
                                  on_release=lambda _: self.master.dialog.content_cls.delete()),
                     MDFlatButton(text="OK", on_release=lambda _: self.master.dialog.content_cls.save())]
        )
        self.master.dialog.open()

    def on_checkbox_switch(self, cb, value):
        self.master.on_checkbox_switch(self.todor, value)

class RightCheckbox(IRightBodyTouch, MDCheckbox):
    pass

class Overview_TestWeek_DayPlanning(DynamicScreen):
    dialog = None
    deldialog = None
    def __init__(self, applr, day, **kwargs):
        self.applr = applr
        self.day = day
        self.required_args = ["applr.id", "day"]
        self.screenname = "overview_testweek_dayplanning"
        super().__init__(required_args=self.required_args, **kwargs)
        self.handle_data()
        self.donedict_orig = {}
        for todor in self.maindata:
            self.append_todo_item(todor)
        self.donedict = copy(self.donedict_orig) # so we can see if sth has actually changed
        self.handle_day_switch()
        self.check_test_dates()

    def append_todo_item(self, todor):
        self.ids.todo.add_widget(DP_ToDoItem(self, todor))
        self.donedict_orig[todor.id] = todor.done

    def handle_day_switch(self):
        items = [
                {"viewclass": "OneLineListItem",
                "text": timestr_with_weekday(day.day), "height": dp(56),
                "on_release": lambda x=day.day: self.show_day(x)}
                for day in self.daylist if day.day != self.day # go through daylist and add items to menuscreen (not the day were already at)
                ]
        self.dayswitch = MDDropdownMenu(items=items, width_mult=4)

    def handle_data(self):
        ob = {"days": ("day",), "dayplanning": ("begintime", "done", "endtime")}
        wh = {"dayplanning": WHERE(date=eq(self.day))}
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY=ob, WHERE=wh) # a TableCollection object with access to table objects
        self.subjecttable = self.branch.master.load(globals.d, self.applr.id)["subjects"]; self.subjectlist = self.subjecttable.data
        self.data_use = [self.tablecoll["days"], self.tablecoll["dayplanning"]]
        self.daytable = self.data_use[0]; self.daylist = self.daytable.data
        self.maintable = self.data_use[1]; self.maindata = self.maintable.data

    def on_checkbox_switch(self, todor, value): # will be called from a todo_item when its checkbox is fired
        self.donedict[todor.id] = value

    def add_todo_item(self):
        self.dialog = MDDialog(
            title="Plan een vak",
            type="custom",
            content_cls=DP_Overview_DialogContent(self),
            buttons=[MDFlatButton(text="CANCEL", on_release=lambda _: self.dialog.dismiss()),
                     MDFlatButton(text="OK", on_release=lambda _: self.dialog.content_cls.save())]
        )
        self.dialog.open()

    def delete_gui(self):
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
        wh = WHERE(day=eq(self.day)) # 3
        self.daytable.delete_row(WHERE=wh) # 3
        wh = WHERE(date=eq(self.day)) # 4
        self.maintable.delete_row(WHERE=wh) # 4

    def save_done(self): # will be called when backbutton is fired (the original func of backbutton will also be called :D)
        if self.donedict == self.donedict_orig: return # nth to save becuz nth changed so we stop this function
        for n, (id, done) in enumerate(self.donedict.items()):
            us = False
            if n == len(self.donedict.items()) - 1: us = True
            wh = WHERE(id=eq(id))
            self.maintable.update(WHERE=wh, done=done, update_screens=us)

    def show_dayswitch(self, caller):
        self.dayswitch.caller = caller
        self.dayswitch.open()

    def show_day(self, day):
        self.dayswitch.dismiss()
        sc = self.branch.screens["overview"]
        globals.sm.show_screen(screen=sc(self.applr, day))

    def check_test_dates(self):
        for subjectr in self.subjectlist:
            if subjectr.testdate == self.day:
                text = "[i]" + ":".join(str(subjectr.time).split(":")[0:2]) + "[b]           "\
                + "Proefwerk " + subjectr.subject
                test_todo_item = OneLineAvatarIconListItem(text=text)
                self.ids.todo.add_widget(test_todo_item)
