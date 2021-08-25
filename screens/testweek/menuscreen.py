from plannings.screens.dynamic_screen import DynamicScreen
import globals
from TypeModels.maininfo import Main
from kivymd.uix.list import OneLineAvatarIconListItem


class OptionItem(OneLineAvatarIconListItem):
    def __init__(self, master, branch=None, **kwargs):
        self.branch = branch # branch that its connected to value is one of the children of branch TestWeek (or TestWeek itself)
        self.master = master
        super().__init__(**kwargs)

class MenuScreen_TestWeek(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.screenname = "menuscreen_testweek"
        self.applr = applr
        super().__init__(**kwargs)
        for child in self.branch.children:
            self.ids.options.add_widget(OptionItem(self, text=child.name, branch=child))
        self.ids.options.add_widget(OptionItem(self, text="Subjects", branch=self.branch))

    def open(self, optionitem_instance):
        globals.sm.show_screen(screen=optionitem_instance.branch.screens["submenuscreen"](self.applr)) # show the main (or subjects) screen of the branch

    def back(self):
        globals.sm.show_previous_screen()
