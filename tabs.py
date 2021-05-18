from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.uix.tabbedpanel import TabbedPanel


Builder.load_file('lfa.kv')
#Builder.load_string('''''')

Window.clearcolor = get_color_from_hex("#808080")

class Tabs(TabbedPanel):
    def selected(self, filename):
        try:
            self.ids.my_image.source = filename[0]
        except:
            pass

    def spinner_clicked(self, value):
        pass
        #self.ids.click_label.text = f'Conversion method you have picked is: {value}'

    checks = []
    def checkbox_clicked(self, instance, value, threshold):
        if value == True:
            Tabs.checks.append(threshold)
            thresh = ''
            for x in Tabs.checks:
                thresh = f'{thresh} {x}'
            #self.ids.output_label.text = f'Thresholding method you have picked is: {thresh}'
            pass
        else:
            Tabs.checks.remove(threshold)
            thresh = ''
            for x in Tabs.checks:
                thresh = f'{thresh} {x}'
            pass

class LFA(App):
    def build(self):
        return Tabs()


if __name__ == '__main__':
    LFA().run()









# darkgray	#A9A9A9	rgb(169,169,169)
# gray	#808080	rgb(128,128,128)
# dimgray	#696969	rgb(105,105,105)



from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.properties import ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.base import runTouchApp
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
