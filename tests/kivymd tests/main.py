from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.screenmanager import ScreenManager

class MainApp(MDApp):
    def build(self):
        return sm

class s1(MDScreen):
    def __init__(self, **kwargs):
        super(s1, self).__init__(**kwargs)
        self.add_widget(MDLabel(text="hello world", halign="center"))

app = MainApp()
sm = ScreenManager()
sm.add_widget(s1(name="1"))
sm.current = "1"

app.run()
