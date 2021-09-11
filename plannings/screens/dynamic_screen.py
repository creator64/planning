from kivy.uix.screenmanager import Screen
from copy import copy

class DynamicScreen(Screen):
    delete_on_leave = False
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = self.get_name()
        self.data_use = []

    def on_enter(self):
        try:
            self.previous_screen # if we have already previous_screen set no need to addign it again
        except AttributeError:
            self.previous_screen = copy(self.manager.previous_screen) # freezing the previous screen at the moment we enter this screen (will be used by BackButton)

    def update(self):
        self.clear_widgets()
        try: self.__init__(self.applr)
        except AttributeError: self.__init__()

    def get_name(self):
        try:
            applid = self.applr.id
        except AttributeError:
            return self.screenname
        return self.screenname + "_" + str(self.applr.id)
