from plannings.screens.dynamic_screen import DynamicScreen
from plannings.time.timestrings import *
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import OneLineListItem
from kivymd.uix.snackbar import Snackbar
import globals


class DP_DayItem(OneLineListItem):
    def __init__(self, master, day, **kwargs):
        self.master = master
        self.day = day
        super().__init__(**kwargs)

    def get_day_str(self):
        return timestr_with_weekday(self.day)

    def show_overview(self):
        screen = self.master.branch.screens["overview"]
        globals.sm.show_screen(screen=screen(self.master.applr, self.day))

class SubMenuScreen_TestWeek_DayPlanning(DynamicScreen):
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek_dayplanning"
        super().__init__(**kwargs)
        self.handle_data()
        for record in self.daylist: # record in form (DateTime.Date Object(y,m,d),)
            self.ids.daylistgui.add_widget(DP_DayItem(self, record.day))

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, self.applr.id, ORDER_BY={"days": ("day",)}) # a TableCollection object with access to table objects
        self.data_use = [self.tablecoll["days"]]
        self.daylist = self.data_use[0].data

    def newday(self):
        dp = MDDatePicker()
        dp.bind(on_save=lambda dp, date, _: self.save(date))
        dp.open()

    def save(self, date):
        daytable = self.data_use[0]
        if daytable.check_value_exist_in_col(col="day", value=date):
            Snackbar(text="Dag bestaat al", duration=1).open()
        else:
            daytable.add_row(day=date)
