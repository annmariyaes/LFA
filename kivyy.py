from kivy.app import App
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.lang import Builder
from kivy.graphics import Color

kvfile = Builder.load_string("""
<MyWidget>:
    Image:
        source: "sample1.jpg"
""")

class MyWidget(Image):
    def on_touch_down(self, touch):
        #self.canvas.add(Rectangle(pos=(touch.x, touch.y), size=(500,100)))
        if touch.is_double_tap:
            print("Double tapped")


class TutorialApp(App):
    def build(self):
        return MyWidget()

if __name__ == "__main__":
    TutorialApp().run()