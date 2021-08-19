from plannings.screens.dynamic_screen import DynamicScreen
import globals

class MenuScreen_TestType(DynamicScreen):
    def __init__(self, applid, **kwargs):
        self.screenname = "menuscreen_testtype"
        self.applid = applid
        super(MenuScreen_TestType, self).__init__(**kwargs)

    def back(self):
        globals.sm.show_previous_screen()
