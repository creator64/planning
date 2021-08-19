from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from _thread import *

class SM(ScreenManager):
    def __init__(self, **kwargs):
        super(SM, self).__init__(**kwargs)

    def show_screen(self, name, direction="left"):
        self.transition.direction = direction
        screen = self.get_screen(name)
        #screen.update()
        self.current = name

    def update_screen(self, name):
        screen = self.get_screen(name)
        screen.reload()

class S1(Screen):
    def __init__(self, reload=False, **kwargs):
        if reload:
            self.clear_widgets()
        super(S1, self).__init__(**kwargs)
        self.ids["bl"].add_widget(Label(text="label made with python"))

    def reload(self):
        self.__init__(reload=True)

class S2(Screen):
    def __init__(self, **kwargs):
        super(S2, self).__init__(**kwargs)

Builder.load_file("style.kv")
sm = SM()
sm.add_widget(S1(name="1")); sm.add_widget(S2(name="2"))
sm.current = "1"

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        return sm

a=MyApp()
a.run()
