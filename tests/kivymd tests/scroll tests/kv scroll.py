from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.list import MDList, OneLineListItem


class MainApp(MDApp):
    def build(self):
        sv = ScrollView()
        ml = MDList()
        sv.add_widget(ml)
        contacts = ["Paula", "John", "Kate", "Vlad"]
        for c in contacts:
            ml.add_widget(
                OneLineListItem(
                    text=c
                )
            )
        return sv

if __name__ == '__main__':
    MainApp().run()
