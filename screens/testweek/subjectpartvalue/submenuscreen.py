from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen

class SubMenuScreen_TestWeek_SubjectPartValue(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek_subjectpartvalue"
        super().__init__(**kwargs)
