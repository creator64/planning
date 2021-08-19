from kivy.uix.screenmanager import ScreenManager as SM
from kivy.uix.screenmanager import ScreenManagerException

class ScreenManager(SM):
    def __init__(self, **kwargs):
        self.previous_screen = None
        #self.outdated_screens = []
        super(ScreenManager, self).__init__(**kwargs)

    def update_screens(self, table):
        for screen in self.screens: # go through all screens that are added
            if table in screen.data_use: # check if the screen makes use of this table (screen.data_use is manually assigned on every screen)
                screen.update()

    def handle_show_screen(f):
        def wrapper(self, *args, **kwargs):
            oldscreen = None
            if self.current: oldscreen = self.get_screen(self.current) # get the screen thats about to change
            success = f(self, *args, **kwargs) # note that self.current changes after this call
            if not success: pass
            else:
                if oldscreen and oldscreen.delete_on_leave:
                    self.remove_widget(oldscreen) # if screen changed successful and oldscreen.delete_on_leave we remove the old screen
            return success
        return wrapper

    @handle_show_screen
    def show_screen(self, name=None, screen=None, direction="left"):
        self.transition.direction = direction
        if name and screen:
            raise Exception("Only one param aloud")
        elif name:
            try: screen = self.get_screen(name)
            except ScreenManagerException:
                raise Exception("Error: No such screen with name %s" %(name))
        elif screen:
            name = screen.name # get name of the screen
            if not self.has_screen(name): # check if screen with that name already exists
                self.add_widget(screen) # if not add the screen
        else:
            raise Exception("Error: need to fill in one of the parameters screen or name")
            return 0
        self.previous_screen = self.current
        #if screen in self.outdated_screens: # if the screen is not updated
        #    screen.update(); self.outdated_screens.remove(screen) # update the screen and remove it from the list of outdated screens
        self.current = name # change the current screen to name
        return 1

    def show_previous_screen(self, direction="right"):
        if self.previous_screen:
            self.show_screen(self.previous_screen, direction=direction)
        else:
            print("ERROR: no previous screen yet")
