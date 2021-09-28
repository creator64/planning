from kivy.uix.screenmanager import Screen
from copy import copy

class DynamicScreen(Screen):
    delete_on_leave = False
    def __init__(self, required_args=["applr.id"], **kwargs):
        super().__init__(**kwargs)
        self.required_args = required_args # a list of arguments that identify a screen
        self.name = self.get_name()
        self.data_use = []

    def on_enter(self):
        try:
            self.previous_screen # if we have already previous_screen set no need to addign it again
        except AttributeError:
            self.previous_screen = copy(self.manager.previous_screen) # freezing the previous screen at the moment we enter this screen (will be used by BackButton)

    def update(self):
        self.clear_widgets()
        args = [vars(self)[arg.split(".")[0]] for arg in self.required_args] # arg could be for ex "applr.id"
        self.__init__(*args)

    def get_name(self):
        l = [self.screenname]
        for arg in self.required_args:
            s = arg.split(".") # so "applr.id" will become ["applr", "id"]
            obj = vars(self)[s[0]] # self.applr
            val=str(obj)
            for attr in s[1:]: # go through all attributes (in out example: ["id"])
                val = str(obj[attr]) # mostly obj is a sqlalchemy record so we can do this, for ex: applr["id"] is possible
            l.append(val)
        return "_".join(l)
