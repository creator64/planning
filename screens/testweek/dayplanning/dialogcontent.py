from plannings.database.where import WHERE, eq
from plannings.time.timecounter import TimeCounter
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.snackbar import Snackbar
from datetime import time as t, datetime as dt


class DP_Overview_DialogContent(MDBoxLayout):
    def __init__(self, master, todor=None, **kwargs):
        self.master = master
        self.todor = todor
        super().__init__(**kwargs)
        if self.todor: self.fill()

    def fill(self):
        bt_h = str(self.todor.begintime.hour); bt_m = str(self.todor.begintime.minute)
        et_h = str(self.todor.endtime.hour); et_m = str(self.todor.endtime.minute)
        if bt_m == "0": bt_m = "00"
        if et_m == "0": et_m = "00" # prevent times like 15:0 or 9:0
        self.ids.begintime.text = bt_h + ":" + bt_m
        self.ids.endtime.text = et_h + ":" + et_m
        self.ids.subject.text = self.todor.subject

    def save(self):
        if self.todor: self.save_update()
        else: self.save_add()

    def save_update(self):
        data = self.collectdata()
        if not data: return 0 # collecting data failed
        maintable = self.master.maintable
        wh = WHERE(id=eq(self.todor.id))
        maintable.update(subject=data["subject"], begintime=data["begintime"],
                          endtime=data["endtime"], WHERE=wh)
        self.master.dialog.dismiss()

    def save_add(self):
        data = self.collectdata()
        if not data: return 0 # collecting data failed
        maintable = self.master.maintable
        maintable.add_row(subject=data["subject"], begintime=data["begintime"],
                          endtime=data["endtime"], done=False, date=self.master.day)
        self.master.dialog.dismiss()

    def delete(self):
        if not self.todor: return 0 # preventing errors
        maintable = maintable = self.master.maintable
        wh = WHERE(id=eq(self.todor.id))
        maintable.delete_row(WHERE=wh)
        self.master.dialog.dismiss()

    def collectdata(self):
        output = {}
        if not self.validation_check():
            Snackbar(text="ongeldige input", duration=1).open()
            return 0
        output["begintime_str"] = self.ids.begintime.text
        output["endtime_str"] = self.ids.endtime.text
        output["subject"] = self.ids.subject.text
        bt_h, bt_m = map(int, self.ids.begintime.text.split(":")); et_h, et_m = map(int, self.ids.endtime.text.split(":"))
        output["begintime"] = t(bt_h, bt_m); output["endtime"] = t(et_h, et_m)
        return output

    def validation_check(self):
        begintime = self.ids.begintime.text; endtime = self.ids.endtime.text
        timeformat = "%H:%M"
        try:
            validtime = dt.strptime(begintime, timeformat) # checking if begintime format is correct
            validtime = dt.strptime(endtime, timeformat) # checking if endtime format is correct
        except ValueError:
            return False

        if not self.ids.subject.text:
            return False # checking if subject textfield is filled
        bt_h, bt_m = begintime.split(":"); et_h, et_m = endtime.split(":")
        tcb = TimeCounter(hours=int(bt_h), minutes=int(bt_m)); tce = TimeCounter(hours=int(et_h), minutes=int(et_m))
        if not tce.get_total_minutes() > tcb.get_total_minutes():
            return False # checking if endtime is later than begintime
        return True
