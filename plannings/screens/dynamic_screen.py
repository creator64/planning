from kivy.uix.screenmanager import Screen

class DynamicScreen(Screen):
    delete_on_leave = False
    def __init__(self, **kwargs):
        super(DynamicScreen, self).__init__(**kwargs)
        self.name = self.get_name()
        self.data_use = []

    def update(self):
        self.clear_widgets()
        self.__init__()

    def get_name(self):
        try:
            applid = self.applid
        except AttributeError:
            return self.screenname
        return self.screenname + "_" + str(self.applid)
