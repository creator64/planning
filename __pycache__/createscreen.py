from plannings.screens.dynamic_screen import DynamicScreen
from kivymd.icon_definitions import md_icons
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.picker import MDDatePicker
from datetime import date as d

class SubjectTab(MDBoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    def __init__(self, subject, learningcontent, date=d.today(), **kwargs):
        self.subject = subject
        self.date = date
        self.learningcontent = learningcontent
        self.title = self.subject
        super(SubjectTab, self).__init__(**kwargs)

    def on_save(self, _, date, _2):
        # _ and _2 are unused
        print(type(date))
        self.date = date
        self.ids.date.text = str(self.date)

    def opendatpicker(self):
        date_dialog = MDDatePicker(day=self.date.day, month=self.date.month, year=self.date.year)
        date_dialog.bind(on_save=self.on_save)#, on_cancel=self.on_cancel)
        date_dialog.open()

class CreateScreen_TestWeek(DynamicScreen):
    def __init__(self, applname, **kwargs):
        self.screenname = "createscreen_testweek"
        self.applname = applname
        super(CreateScreen_TestWeek, self).__init__(**kwargs)
        self.ids.tabs.add_widget(SubjectTab(subject="math", learningcontent="lol"))
        self.ids.tabs.add_widget(SubjectTab(subject="physics", learningcontent="haha"))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
