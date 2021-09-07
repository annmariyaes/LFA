import kivy
kivy.require('1.0.7')

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import ObjectProperty, BooleanProperty
from kivy.lang import Builder

Builder.load_string('''
<Scroller>
    # root is Scroller here
    # create a new ObjectProperty in kv that holds the ref to Gridlayout
    # so you can access the instance in python code
    view: glayout
    GridLayout:
        id: glayout
        cols: 1
        size_hint: (1, None)
        height: self.minimum_height

<Field>
    canvas.before:
        Color:
            rgba: (0.2, 0.2, 0.2, 1) if self.bg else (0.1, 0.1, 0.1, 1)
        Rectangle:
            # binding properties is done implicitly and instructions aren't
            # piled up while doing that.
            pos: self.pos
            # self here refers to Field as `self` is supposed to refer to the
            # Widget not the drawing instruction
            size: self.size
    rows: 1
    padding: 10
    size: (0, 60)
    size_hint: (1, None)
    Label:
        text: root.name
    Button:
        text: 'test button'
        size: (200, 0)
        size_hint: (None, 1)
''')


class Main(App):

    def build(self):
        self.root = GridLayout(rows = 1)
        self.root.add_widget(Scroller())
        return self.root


class Scroller(ScrollView):
    def __init__(self, **kwargs):
        super(Scroller, self).__init__(**kwargs)
        for i in range(20):
            # access self.view that was set in kv
            self.view.add_widget(
                                Field(
                                    name = 'Test field {}'.format(i),
                                    bg = i%2 is 0))

class Field(GridLayout):

    # use  kivy's Properties so it becomes easier to observe and apply changes
    # as a plus these can also be directly used in kv. As a advantage of using this now
    # you can change name and bg dynamically and the changes should be reflected on
    # screen
    name = ObjectProperty('Test field uninitialized')

    bg = BooleanProperty(False)


if __name__ in ('__main__', '__android__'):
    app = Main()
    app.run()