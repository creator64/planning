from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton

class BackButton(MDRaisedButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "back"

    def on_release(self):
        app = MDApp.get_running_app() # get app
        sm = app.root # get screenmanager
        sm.show_screen(sm.get_screen(sm.current).previous_screen, direction="right") # get the current screen and its (frozen) previous_screen and show it
