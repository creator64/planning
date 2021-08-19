from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.list import OneLineAvatarIconListItem
from kivymd.uix.dialog import MDDialog
import globals

class ItemType(OneLineAvatarIconListItem):
    divider = None

    def set_icon(self, instance_check):
        instance_check.active = True
        check_list = instance_check.get_widgets(instance_check.group)
        for check in check_list:
            if check != instance_check:
                check.active = False

class Content(BoxLayout):
    def __init__(self, **kwargs):
        super(Content, self).__init__(**kwargs)
        for type in globals.types:
            self.ids.itemtypes.add_widget(ItemType(text=type.name))