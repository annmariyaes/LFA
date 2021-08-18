from kivy.lang import Builder
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.graphics import Point
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen

Builder.load_string("""

<MyScreenManager>:
    ThirdScreen:
        id: third_screen

<ThirdScreen>:
    name: '_third_screen_'
    id: third_screen
    BoxLayout:
        orientation: "vertical"
        id: third_screen_boxlayout
        Label:
            id: main_title
            text: "Title"
            size_hint: (1, 0.1)
        BoxLayout:
            id: image_box_layout
            Image:
                id: main_image
                source: "sample1.jpg"
            Widget:
                id: image_canvas
                size_hint: (0.0000001, 0.0000001)
                canvas:
                    Rectangle:
                        id: root.rect_box
                        pos: (root.x1, root.y1)
                        size: (root.t_x, root.t_y)
        BoxLayout:
            id: button_boxlayout
            orientation: "horizontal"
            padding: 10
            size_hint: (1, 0.15)
            Button:
                id: accept_button
                text: "Okay"
                size_hint: (0.33, 1)
                on_press: root.image_accepted_by_user(root.image_address)
            Button:
                id: crop_button
                text: "Crop"
                size_hint: (0.33, 1)
                on_press: root.enable_cropping()
            Button:
                id: cancel_button
                text: "Cancel"
                size_hint: (0.33, 1) 
                on_press: root.manager.current = '_first_screen_'
""")

class MyScreenManager(ScreenManager):
    pass

class ThirdScreen(Screen):
    rect_box = ObjectProperty(None)
    t_x = NumericProperty(0.0)
    t_y = NumericProperty(0.0)
    x1 = y1 = x2 = y2 = NumericProperty(0.0)

    def enable_cropping(self):
        print("\nThirdScreen:")
        print(self.ids.main_image.pos)
        print(self.ids.main_image.size)
        print("\tAbsolute size=", self.ids.main_image.norm_image_size)
        print("\tAbsolute pos_x=", self.ids.main_image.center_x - self.ids.main_image.norm_image_size[0] / 2.)
        print("\tAbsolute pos_y=", self.ids.main_image.center_y - self.ids.main_image.norm_image_size[1] / 2.)

    def on_touch_down(self, touch):
        self.x1 = touch.x
        self.y1 = touch.y
        self.t_x = touch.x
        self.t_y = touch.y

        touch.grab(self)
        print(self.x1, self.y1)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            # not working
            self.t_x = touch.x
            self.t_y = touch.y

            print(self.t_x, self.t_y)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # final position
            self.x2 = touch.x
            self.y2 = touch.y

            print(self.x2, self.y2)

class MyApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()