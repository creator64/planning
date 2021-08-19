from kivy.app import App
from kivy.lang.builder import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen as s

class globs:
    def __init__(self, var):
        self.var = var

g = globs("apenzooi")

class Screen(s):
    def __init__(self, **kwargs):
        super(Screen, self).__init__(**kwargs)

    def update(self):
        self.ids["l"].text = g.var
        print(f"screen {self.name} is updated")


class WindowManager(ScreenManager):
    def __init__(self, **kwargs):
        super(WindowManager, self).__init__(**kwargs)

    def show_screen(self, name, direction="left"):
        self.transition.direction = direction
        screen = self.get_screen(name)
        screen.update()
        self.current = name

class Home(Screen):
    def __init__(self, **kwargs):
        super(Home, self).__init__(**kwargs)
        self.ids["l"].text = g.varvar

class Settings(Screen):
    def __init__(self, **kwargs):
        super(Settings, self).__init__(**kwargs)
        self.ids["l"].text = g.var

    def save(self):
        g.var = self.ids["l"].text
        print(f"Data is saved. Changes: {g.var=}")

Builder.load_file("style.kv")

sm = WindowManager()
screens = [Home(name='home'), Settings(name='settings')]
sm.add_widget(screens[0]); sm.add_widget(screens[1])

sm.current = 'home'

class MyApp(App):
    def __init__(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)

    def build(self):
        return sm


if __name__ == '__main__':
    MyApp().run()
