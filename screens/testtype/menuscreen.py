from plannings.screens.dynamic_screen import DynamicScreen
import globals

class MenuScreen_TestType(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.screenname = "menuscreen_testtype"
        self.applr = applr
        super(MenuScreen_TestType, self).__init__(**kwargs)
