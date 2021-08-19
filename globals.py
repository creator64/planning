from TypeModels.testtype import TestType
from TypeModels.testweek import TestWeek
from TypeModels.maininfo import Main
from plannings.screens.screenmanager import ScreenManager # custom screenmanager inheriting from kivy screenmanager
from plannings.database.db import DB
from plannings.database.where import WHERE, eq
from kivymd.app import MDApp

"""stores global variables which every file has access to"""

class MainApp(MDApp):
    def build(self):
        #self.theme_cls.primary_palette = "BlueGray"
        return sm

# variables
app = MainApp()
sm = ScreenManager()
types = [TestType, TestWeek]
d = DB("data.db", sm=sm)
version = "0.0"

# functions

def get_next_application_id():
    appltable = Main.load(d)["applications"]
    try: id = list(appltable.data)[-1][0]
    except IndexError:
        return 1 # if empty list we get index error and it means there arent any applications yet so we just return 1
    return id + 1

def get_applid(applname):
    wh = WHERE(name=eq(applname)) # create a where object (name==applname)
    # get the id of the first (and only) record that we have selected (where name is the given applname)
    applid = Main.load(d, WHERE={"applications": wh})["applications"].data.fetchone()["id"]
    return applid

def get_type(typename):
    try: return [t for t in types if t.name == typename][0] # go through all types and select the one with the right name
    except IndexError: return None

# end
