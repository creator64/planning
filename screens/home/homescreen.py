from plannings.screens.dynamic_screen import DynamicScreen # custom screen inheriting from kivymd screen
from plannings.database.where import WHERE, eq
from TypeModels.maininfo import Main
from screens.home.dialogcontent import Content
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomsheet import MDListBottomSheet
from kivymd.uix.list import TwoLineAvatarIconListItem
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.snackbar import Snackbar
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from globals import sm, d
import globals


class ApplItem(TwoLineAvatarIconListItem):
    def __init__(self, name, type, id, master, **kwargs):
        super(ApplItem, self).__init__(**kwargs)
        self.master = master
        self.name = name; self.text = name
        self.type = type; self.secondary_text = type
        self.id = id

class HomeScreen(DynamicScreen):
    dialog = None
    dialogdel = None
    dialogedit = None
    overlay_color = get_color_from_hex("#6042e4")
    def __init__(self, **kwargs):
        self.screenname = "home"
        self.mode = "normal"
        super(HomeScreen, self).__init__(**kwargs)
        self.handle_data()
        for row in self.data: # go through all applications
            name, type, id = row["name"], row["type"], row["id"]
            self.ids.appl_list.add_widget(ApplItem(name=name, type=type, id=id, master=self))
        self.ids.box.add_widget(MDFlatButton(text="add some data", on_release=lambda x: self.data_use[0].add_row(name="lol", type="vet")))

    def handle_data(self):
        self.branch = Main
        self.tablecoll = self.branch.load(d) # a TableCollection object with access to table objects
        self.data_use = [self.tablecoll["applications"]]
        self.data = self.data_use[0].data # get data of table applications

    def change_toolbar(self, text=None, color=None, left_actions=None, right_actions=None):
        if text!=None: self.ids.toolbar.title = text
        if left_actions!=None: self.ids.toolbar.left_action_items = left_actions
        if right_actions!=None: self.ids.toolbar.right_action_items = right_actions
        if color!=None: Animation(md_bg_color=color, d=0.2).start(self.ids.toolbar)

    def trigger_normal_mode(self):
        self.mode = "normal"
        self.change_toolbar("Home", (0,0,0,1), [])

    def trigger_delete_mode(self):
        self.mode = "delete"
        l = [["close", lambda x: self.trigger_normal_mode()]]
        self.change_toolbar("Select a planning to delete", (1,0,0,1), l)

    def trigger_editname_mode(self):
        self.mode = "editname"
        l = [["close", lambda x: self.trigger_normal_mode()]]
        self.change_toolbar("Select a planning to rename", (0,0,1,1), l)

    def on_appl_click(self, applitem):
        print(applitem.id)
        if self.mode == "normal":
            self.open(applitem)
        elif self.mode == "delete":
            self.delete_gui(applitem)
        elif self.mode == "editname":
            self.editname_gui(applitem)

    def open(self, applitem):
        type = globals.get_type(applitem.type)
        applid = applitem.id
        sm.show_screen(screen=type.menuscreen(applid))

    def delete_gui(self, applitem):
        self.dialogdel = MDDialog(text="Are you sure you want to delete planning %s" %(applitem.name),
                 buttons=[MDFlatButton(text="CANCEL", on_release=lambda x: self.dialogdel.dismiss()),
                          MDFlatButton(text="DELETE", on_release=lambda x: self.delete(applitem))])
        self.dialogdel.open()

    def delete(self, applitem):
        appltable = self.data_use[0] # get Main_applications
        branch = globals.get_type(applitem.type) # get the branch object
        branch.delete(globals.d, applid=applitem.id) # delete this branch
        print(f"deleted appl {applitem.name} with id {applitem.id}")
        wh = WHERE(id=eq(applitem.id)) # make a where object (id==applitem.id)
        appltable.delete_row(wh) # delete the record of Main_applications where we save info of this application
        self.dialogdel.dismiss() # close the dialog
        Snackbar(text="Planning removed successfully", md_bg_color=(0,1,0,1), duration=1).open() # confirmation

    def editname_gui(self, applitem):
        self.dialogedit = MDDialog(
                title="choose a new name",
                type="custom",
                content_cls=MDTextField(text=applitem.name, hint_text="name"),
                buttons=[MDFlatButton(text="CANCEL", on_release=lambda x: self.dialogedit.dismiss()),
                         MDFlatButton(text="SAVE", on_release=lambda x: self.editname(applitem, self.dialogedit.content_cls.text))])
        self.dialogedit.open()

    def editname(self, applitem, newname):
        appltable = self.data_use[0] # get Main_applications
        wh = WHERE(id=eq(applitem.id)) # make a where object (id==applitem.id)
        appltable.update(WHERE=wh, name=newname) # update the name of this application
        self.dialogedit.dismiss() # close the dialog
        Snackbar(text="Planning renamed successfully", md_bg_color=(0,1,0,1), duration=1).open() # confirmation


    def new(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="New planning",
                type="custom",
                content_cls=Content(),
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        on_release=lambda x: self.dialog.dismiss()
                    ),
                    MDFlatButton(
                        text="NEXT",
                        on_release=lambda x: self.next(self.dialog)
                    ),
                ],
            )
        self.dialog.open()

    def next(self, dialog):
        itemtypes = dialog.content_cls.ids.itemtypes.children # get all list items representing a type
        applname=self.dialog.content_cls.ids.applname.text # get application name
        if not applname:
            Snackbar(text="No name filled", duration=1).open()
            return 0
        typename = ""
        for itemtype in itemtypes: # go through all items
            if itemtype.ids.check.active: # check if checkbox is active
                typename = itemtype.text # get name of type
                break
        type = globals.get_type(typename)
        if not type: # no type selected
            Snackbar(text="No type selected", duration=1).open()
            return 0
        dialog.dismiss() # close the dialog (otherwise it shows up on the next screen)
        # show the createscreen of the selected type which handles the rest of the process
        sm.show_screen(screen=type.createscreen(applname))
        return 1
