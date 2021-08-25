from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen
from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from datetime import date as d
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker
import globals


class SubjectDialogContent(MDBoxLayout):
    def __init__(self, subjectitem, **kwargs):
        self.subjectitem = subjectitem
        super().__init__(**kwargs)

    def opendatepicker(self):
        date_dialog = MDDatePicker(day=self.subjectitem.date.day, month=self.subjectitem.date.month, year=self.subjectitem.date.year)
        date_dialog.bind(on_save=self.save_date)
        date_dialog.open()

    def save_date(self, _, date, _2):
        # _ and _2 are unused
        self.ids.date.text = "current date: " + str(date)

class SubjectItem(ThreeLineAvatarListItem):
    def __init__(self, master, subjectr, **kwargs):
        self.master = master
        self.subjectr = subjectr
        super().__init__(**kwargs)

    def get_date(self):
        wd = self.date.weekday()
        dict = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
        monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        return f"{dict[wd]} {self.date.day} {monthDict[self.date.month]}"

    def get_image(self):
        return "math.jpg"

class SubMenuScreen_TestWeek(DynamicScreen):
    dialog = None
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek"
        self.handle_data()
        super().__init__(**kwargs)
        for subject in self.data:
            self.ids.subjectlist.add_widget(SubjectItem(self, subject))

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, applid=self.applr.id) # a TableCollection object with access to table objects
        self.data_use = [self.tablecoll["subjects"]] # specify the tables we use for the update system
        self.data = self.data_use[0].data # get data of subjects applications

    def edit_subject(self, subjectitem):
        self.dialog = MDDialog(title="edit subject", type="custom", content_cls=SubjectDialogContent(subjectitem),  buttons=[
                    MDRaisedButton(
                        text="CANCEL", on_release=lambda _: self.dialog.dismiss()
                    ),
                    MDRaisedButton(
                        text="OK", on_release=lambda _: self.save(subjectitem)
                    ),
                ],)
        self.dialog.open()

    def save(self, subjectitem):
        print("lol")
