from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class MyScrollView(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

theRoot = Builder.load_string('''
#: import Window kivy.core.window.Window
MyScrollView:
    ScrollView:
        id: inner_scroll
        bar_width: 5
        scroll_type: ['bars', 'content']
        do_scroll: (True, False)
        size_hint_y: None
        effect_cls: "ScrollEffect"
        #height: Window.height/4.5
        GridLayout:
            id: horizontal_grid
            rows: 3
            padding: [10, 10]
            size: self.minimum_size
            size_hint: None, 1
''')



class ScrollTwoApp(App):
    def build(self):
        Clock.schedule_once(self.add_members)
        return theRoot

    def add_members(self, dt):
        for i in range(25):
            #theRoot.ids.main_box.add_widget(Label(text='label'+str(i), size_hint=(1.0, None), height=25))
            theRoot.ids.horizontal_grid.add_widget(Label(text='' + str(i), size_hint=(None, 1), width=90))


ScrollTwoApp().run()
