from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from load_kv import load_kv

load_kv("screens")
from screens.type1.screen1.screen1 import Screen1
from screens.type1.screen2.screen2 import Screen2
from screens.screen3.screen3 import Screen3



class SM(ScreenManager):
    pass


sm = SM()
sm.add_widget(Screen1(name="1"))
sm.current = "1"


class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        
    def build(self):
        return sm

if __name__ == '__main__':
    MyApp().run()
