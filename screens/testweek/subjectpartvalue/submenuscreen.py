from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen
from plannings.database.where import WHERE, eq
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
import globals


class SPV_Value_Button(MDFlatButton):
    dialog = None
    def __init__(self, master, subject, part, value, found: bool, **kwargs):
        self.master = master
        self.subject = subject
        self.part = part
        self.value = value
        self.found = found
        super().__init__(**kwargs)
        if self.found: self.text = str(self.value)
        else: self.text = "0"

    def on_release(self):
        if not self.dialog:
            self.dialog = MDDialog(title=f"verander lengte voor het onderdeel {self.part} van {self.subject}", type="custom",
                               buttons=[
                                    MDFlatButton(text="CANCEL", on_release=lambda _: self.dialog.dismiss()),
                                    MDFlatButton(text="UPDATE", on_release=lambda _: self.update_value())],
                               content_cls=MDTextField(text=str(self.value)))
        self.dialog.open()

    def check(self, value):
        if not value.isdigit():
            return False
        return True

    def update_value(self):
        value = self.dialog.content_cls.text
        if not self.check(value):
            Snackbar(text="Invullig moet een geheel getal zijn van 0 of hoger", duration=1.2).open()
            return 0 # no correct value so stop the function (from updating)
        self.text = value; self.value = value
        self.update_in_db()
        self.dialog.dismiss()

    def update_in_db(self):
        maintable = self.master.maintable
        if self.found:
            wh = WHERE(subject=eq(self.subject), part=eq(self.part))
            maintable.update(WHERE=wh, value=self.value, update_screens=False)
        else:
            maintable.add_row(subject=self.subject, part=self.part, value=self.value, update_screens=False)
            self.found = True

class SPV_Part_Button(MDFlatButton):
    dialog = None
    def __init__(self, master, part, **kwargs):
        self.master = master
        self.part = part
        super().__init__(**kwargs)

    def on_release(self):
        if not self.dialog:
            self.dialog = MDDialog(title="verander naam onderdeel", type="custom",
                               buttons=[
                                    MDFlatButton(text="CANCEL", on_release=lambda _: self.dialog.dismiss()),
                                    MDFlatButton(text="UPDATE", on_release=lambda _: self.update_name())],
                               content_cls=MDTextField(text=self.part))
        self.dialog.open()

    def check(self, partname):
        if self.master.parttable.check_value_exist_in_col("part", partname):
            return False, "NameExistanceError"
        elif partname == "":
            return False, "NoNameError"
        return True, "NoError"

    def update_name(self):
        newpartname = self.dialog.content_cls.text
        correctname = self.check(newpartname) # (False, "KindOfError") or (True, "NoError")
        if not correctname[0]:
            if correctname[1] == "NameExistanceError":
                Snackbar(text="Deze naam bestaat al", duration=1.2).open()
            else:
                Snackbar(text="Geen naam ingevuld", duration=1.2).open()
            return 0 # no correct name so stop the function (from updating)
        parttable = self.master.parttable
        maintable = self.master.maintable
        wh = WHERE(part=eq(self.part)) # self.part is still the old partname
        parttable.update(WHERE=wh, part=newpartname, update_screens=False) # update the partname in the parttable
        maintable.update(WHERE=wh, part=newpartname, update_screens=True) # update the part column in the maintable
        self.dialog.dismiss()

class SubMenuScreen_TestWeek_SubjectPartValue(DynamicScreen):
    dialog = None
    def __init__(self, applr, **kwargs):
        self.applr = applr
        self.screenname = "submenuscreen_testweek_subjectpartvalue"
        self.handle_data()
        super().__init__(**kwargs)
        self.data_use = [self.parttable, self.maintable, self.subjecttable] # cant to it in handle_data becuz itll get overwritten
        self.organise_cells()

    def organise_cells(self):
        self.ids.grid.add_widget(MDLabel())
        for subjectr in self.subjectlist:
            self.ids.grid.add_widget(MDLabel(text="[i][size=20]" + subjectr.subject, markup=True))
        for partr in self.partlist:
            self.ids.grid.add_widget(SPV_Part_Button(self, partr.part))
            for subjectr in self.subjectlist:
                spvr = self.findrecord(partr.part, subjectr.subject)
                if spvr:
                    self.ids.grid.add_widget(SPV_Value_Button(self, *spvr, found=True))
                else: self.ids.grid.add_widget(SPV_Value_Button(self, subjectr.subject, partr.part, 0, found=False))

    def findrecord(self, part, subject): # returns (subject, part, value) if found otherwise None
        for spvr in self.maindata:
            if spvr.subject == subject and spvr.part == part:
                return spvr
        return None

    def handle_data(self):
        self.tablecoll = self.branch.load(globals.d, applid=self.applr.id) # a TableCollection object with access to table objects
        ob = {"subjects": ("testdate", "time")}
        self.subjecttable = self.branch.master.load(globals.d, applid=self.applr.id, ORDER_BY=ob)["subjects"]; self.subjectlist = self.subjecttable.data
        self.parttable = self.tablecoll["parts"]; self.maintable = self.tablecoll["subjectpartvalue"]
        self.partlist = self.parttable.data; self.maindata = self.maintable.data

    def show_part_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(title="voeg toe of verwijder een nieuw onderdeel", type="custom",
                                   buttons=[
                                        MDFlatButton(text="DELETE", theme_text_color="Custom", text_color="red", on_release=lambda _: self.delete_part()),
                                        MDFlatButton(text="ADD", on_release=lambda _: self.add_part())],
                                   content_cls=MDTextField(hint_text="naam van onderdeel"))
        self.dialog.open()

    def add_part(self):
        part = self.dialog.content_cls.text
        if not part: # check if the textfield is empty
            Snackbar(text="Kan geen leeg onderdeel toevoegen", duration=1.2).open() # make to the user clear that an empty part isnt possible
            return 0 # stop the function
        if self.parttable.check_value_exist_in_col("part", part): # check if the value of part already exists
            Snackbar(text="Dit onderdeel bestaat al", duration=1.2).open() # make to the user clear it exists
            return 0 # stop the function
        self.parttable.add_row(part=part)
        self.dialog.content_cls.text="" # clear the text
        self.dialog.dismiss()

    def delete_part(self):
        part = self.dialog.content_cls.text
        if not self.parttable.check_value_exist_in_col("part", part): # check if the value of part does exists
            Snackbar(text="Dit onderdeel bestaat niet", duration=1.2).open() # make to the user clear it doesnt exists
            return 0 # stop the function
        self.parttable.delete_row(WHERE=WHERE(part=eq(part)))
        self.dialog.content_cls.text="" # clear the text
        self.dialog.dismiss()
