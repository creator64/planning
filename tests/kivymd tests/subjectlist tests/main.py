from kivymd.app import MDApp
from kivymd.uix.list import ThreeLineAvatarListItem
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from datetime import date as d
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.picker import MDDatePicker

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
    def __init__(self, master, subject, learningcontent, date, mark, **kwargs):
        self.master = master
        self.subject = subject
        self.learningcontent = learningcontent
        self.date = date
        self.mark = mark
        super().__init__(**kwargs)

    def get_date(self):
        wd = self.date.weekday()
        dict = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
        monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        return f"{dict[wd]} {self.date.day} {monthDict[self.date.month]}"

    def get_image(self):
        return "math.jpg"

class sm(ScreenManager):
    pass

class s1(Screen):
    dialog = None
    def __init__(self, data, **kwargs):
        self.data = data
        super().__init__(**kwargs)
        for subject in self.data:
            self.ids.subjectlist.add_widget(SubjectItem(self, *subject))

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
        b = self.dialog.content_cls.ids
        subjectitem.subject = b.subject.text
        subjectitem.mark = float(b.mark.text)
        subjectitem.learningcontent = b.learningcontent.text
        year, month, day = b.date.text.replace("current date: ", "").split("-")
        subjectitem.date = d(int(year), int(month), int(day))
            

class Example(MDApp):
    def build(self):
        return s

Builder.load_file("style.kv")

data = [("Math", "H1, H2, H3 en en K-opdrachten", d(2021, 9, 23), 9.9), ("biologie", "ik heb dit vak niet eens lol", d(2021, 9, 23), 3)]
e = Example()
s = sm()
s.add_widget(s1(data, name="lol"))

e.run()
