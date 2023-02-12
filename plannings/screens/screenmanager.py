from kivy.uix.screenmanager import ScreenManager as SM
from kivy.uix.screenmanager import ScreenManagerException
import time
from _thread import start_new_thread

class ScreenManager(SM):
    def __init__(self, **kwargs):
        self.previous_screen = None
        self.deltime = 60 # see self.screen_deleting
        self.screen_deleting = True # When this is set to True every screen will be deleted after <self.deltime> seconds
        super(ScreenManager, self).__init__(**kwargs)
        #start_new_thread(self.screen_del_handle, ()) bugged for now

    def update_screens(self, table):
        for screen in self.screens: # go through all screens that are added
            if table in screen.data_use: # check if the screen makes use of this table (screen.data_use is manually assigned on every screen)
                screen.update()
                #self.remove_widget(screen)

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
        new = False
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
                new = True
        else:
            raise Exception("Error: need to fill in one of the parameters screen or name")
            return 0
        self.previous_screen = self.current
        self.current = name # change the current screen to name
        screen.last_visited = 0 # reset when the screen was last_visited
        try: screen.entering(new) # self made event # param new points if the screen has not been given before
        except AttributeError: pass
        return 1

    def show_previous_screen(self, direction="right"):
        if self.previous_screen:
            self.show_screen(self.previous_screen, direction=direction)
        else:
            print("ERROR: no previous screen yet")

    def screen_del_handle(self):
        while (self.screen_deleting):
            for screen in self.screens:
                if self.get_screen(self.current) == screen: # preventing a screen getting deleted while we are on that screen
                    continue                                # and keeping last_visited of the screen on 0 while we are on that screen
                elif screen.last_visited > self.deltime:
                    if not screen.permanent:
                        self.remove_widget(screen)
                screen.last_visited += 5
                print(screen.name, screen.last_visited)
            print("---------------")
            time.sleep(5)
