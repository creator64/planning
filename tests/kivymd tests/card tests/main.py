from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivymd.uix.card import MDCard
from datetime import date as d
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField


Builder.load_string('''
<SubjectCard>:
    orientation: "vertical"
    size_hint: .80, None
    size: "200dp", "500dp"
    pos_hint: {"center_x": .5, "center_y": .5}
    elevation: 20
    md_bg_color: 1,1,1,1
    radius: [15,]

    FitImage:
        source: 'math.jpg'
        size_hint_y: 4
        radius: 15, 15, 0, 0
        pos_hint: {"top": 1}

    MDLabel:
        text: root.subject
        theme_text_color: "Secondary"
        adaptive_height: True
        bold: True
        color: (0,0,0,1)
        font_size: 25
        halign: "center"

    MDSeparator:
        height: "1dp"

    MDGridLayout:
        cols: 2
        MDLabel:
            text: "Date:"
            size_hint: 0.1, 1
            bold: True
            font_size: root.fs
        MDLabel:
            id: date
            size_hint: 0.8, 1
            text: root.get_date()
            halign: "center"
            font_size: root.fs
        MDLabel:
            text: "Mark:"
            size_hint: 0.3, 1
            bold: True
            font_size: root.fs
        MDLabel:
            id: mark
            text: "Body2"
            size_hint: 0.7, 1
            text: str(root.mark)
            halign: "center"
            font_size: root.fs
    MDLabel:
        text: root.learningcontent
        italic: True
''')

class SubjectCard(MDCard):
    def __init__(self, subject, learningcontent, date, mark, **kwargs):
        self.subject = subject
        self.learningcontent = learningcontent
        self.date = date
        self.mark = mark
        self.fs = 19
        super().__init__(**kwargs)

    def get_date(self):
        wd = self.date.weekday()
        dict = {0: "monday", 1: "tuesday", 2: "wednesday", 3: "thursday", 4: "friday", 5: "saturday", 6: "sunday"}
        monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
        return f"{dict[wd]} {self.date.day} {monthDict[self.date.month]}"

class sm(ScreenManager):
    pass

class s1(Screen):
    dialog = None
    def __init__(self, subject, learningcontent, date, mark, **kwargs):
        super().__init__(**kwargs)
        l = [subject, learningcontent, date, mark]
        self.subjectcard = SubjectCard(*l); self.add_widget(self.subjectcard)
        self.add_widget(MDRaisedButton(text="edit", on_release=lambda _: self.edit()))

    def edit(self):
        box = MDBoxLayout(orientation="vertical")
        box.add_widget(MDTextField(text=str(self.subjectcard.mark), hint_text="mark"))
        box.add_widget(MDTextField(text=self.subjectcard.learningcontent, hint_text="description", multiline=True))
        self.dialog = MDDialog(title="edit subject", type="custom", content_cls=box,  buttons=[
                    MDRaisedButton(
                        text="CANCEL"
                    ),
                    MDRaisedButton(
                        text="OK"
                    ),
                ],)
        self.dialog.open()

class Example(MDApp):
    def build(self):
        return s

data = [("Math", "H1, H2, H3 en en K-opdrachten", d(2021, 9, 23), 9.9), ("biologie", "ik heb dit vak niet eens lol", d(2021, 9, 23), 3)]
e = Example()
s = sm()
s.add_widget(s1(*data[0], name="lol"))

e.run()
