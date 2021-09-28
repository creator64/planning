from kivymd.uix.card import MDCardSwipe
from kivy.lang import Builder

KV = '''
<SwipeToDeleteListItem>:
    size_hint_y: None
    #height: content.height

    MDCardSwipeLayerBox:
        padding: "8dp"

        MDIconButton:
            icon: "trash-can"
            pos_hint: {"center_y": .5}

    MDCardSwipeFrontBox:
        id: frontbox
'''

class SwipeToDeleteListItem(MDCardSwipe):
    '''Card with `swipe-to-delete` behavior.'''
    def __init__(self, listitem, **kwargs):
        self.listitem = listitem
        super().__init__(**kwargs)
        self.ids.frontbox.add_widget(listitem)

Builder.load_string(KV)
