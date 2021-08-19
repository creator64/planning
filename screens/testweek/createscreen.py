from plannings.screens.dynamic_screen import DynamicScreen
from kivymd.icon_definitions import md_icons
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.boxlayout import MDBoxLayout

class SubjectTab(MDBoxLayout, MDTabsBase):
    '''Class implementing content for a tab.'''
    def __init__(self, subject, date, learningcontent, **kwargs):
        self.subject = subject
        self.date = date
        self.learningcontent = learningcontent
        self.title = self.subject
        super(SubjectTab, self).__init__(**kwargs)

class CreateScreen_TestWeek(DynamicScreen):
    def __init__(self, applname, **kwargs):
        self.screenname = "createscreen_testweek"
        self.applname = applname
        super(CreateScreen_TestWeek, self).__init__(**kwargs)
        self.ids.tabs.add_widget(SubjectTab(subject="math", learningcontent="lol", date=1))
        self.ids.tabs.add_widget(SubjectTab(subject="physics", learningcontent="haha", date=1))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        '''
        Called when switching tabs.

        :type instance_tabs: <kivymd.uix.tab.MDTabs object>;
        :param instance_tab: <__main__.Tab object>;
        :param instance_tab_label: <kivymd.uix.tab.MDTabsLabel object>;
        :param tab_text: text or name icon of tab;
        '''
        # get the tab icon.
        count_icon = instance_tab.subject
        # print it on shell/bash.
        print(f"Welcome to {count_icon}' tab'")
