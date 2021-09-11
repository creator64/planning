from plannings.screens.dynamic_screen import DynamicScreen
from TypeModels.maininfo import Main
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelOneLine
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton
from kivy.uix.scrollview import ScrollView
import weakref
import globals


class ContentPersons(ScrollView): pass
class ContentTasks(ScrollView): pass

class CreateScreen_TestType(DynamicScreen):
    delete_on_leave = False
    def __init__(self, applname, **kwargs):
        self.screenname = "createscreen_testtype"
        self.applname = applname
        super().__init__(**kwargs)
        personpanel = MDExpansionPanel(
            icon="account",
            content=ContentPersons(),
            panel_cls=MDExpansionPanelOneLine(
                text="Persons",
            ))
        taskpanel = MDExpansionPanel(
            icon="profile",
            content=ContentTasks(),
            panel_cls=MDExpansionPanelOneLine(
                text="Tasks",
            ))
        self.ids.panels.add_widget(personpanel); self.ids.panels.add_widget(taskpanel)
        self.ids.panels.ids['personpanel'] = weakref.ref(personpanel); self.ids.panels.ids['taskpanel'] = weakref.ref(taskpanel)

    def add_person(self):
        panel = self.ids.panels.ids.personpanel.content.ids.personlist # get panel object
        name = self.ids.person_name; age = self.ids.person_age # get textfiels objects for name and age
        if age.text.isdigit() and name.text:
            panel.add_widget(TwoLineListItem(text=name.text, secondary_text=age.text))
            name.text = ""; age.text = ""
        else:
            Snackbar(text="invalid age or name", duration=1).open()

    def add_task(self):
        panel = self.ids.panels.ids.taskpanel.content.ids.tasklist # get panel object
        task = self.ids.task_task; timeneeded = self.ids.task_timeneeded # get textfield objects for task and timeneeded
        if timeneeded.text.isdigit() and task.text:
            panel.add_widget(TwoLineListItem(text=task.text, secondary_text=f"time: {timeneeded.text}"))
            task.text = ""; timeneeded.text = ""
        else:
            Snackbar(text="invalid taskname or time", duration=1).open()

    def save(self):
        applid = globals.get_next_application_id()
        globals.add_application(self.branch, self.applname, show=False) # (self.branch is assigned in Tree.handle_branches)

        tasktable, persontable = self.branch.load(globals.d, applid=applid).tables[0:2] # get persontable and tasktable weve just created
        taskdata = self.ids.panels.ids.taskpanel.content.ids.tasklist.children # get task data
        persondata = self.ids.panels.ids.personpanel.content.ids.personlist.children # get person data
        for record in persondata: # 3 (records are list item objects)
            persontable.add_row(name=record.text, age=record.secondary_text)
        for record in taskdata:
            tasktable.add_row(task=record.text, timeneeded=record.secondary_text)
        globals.sm.show_screen(screen=self.branch.menuscreen(applid))
