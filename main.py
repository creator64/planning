from plannings.screens.loadkv import LoadKv
from screens.home.homescreen import HomeScreen
from globals import app, sm, d
from TypeModels.maininfo.branches import Main

#Main.create(globals.d)

LoadKv("screens") # loads all kv files in directory screens

sm.show_screen(screen=HomeScreen())

app.run()
