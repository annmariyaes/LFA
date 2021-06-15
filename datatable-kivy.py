from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivymd.uix.datatables import MDDataTable


Builder.load_string('''
<MyDataTable>
    id: table1
    size_hint: [0.9, 0.6]
    use_pagination: True
<MyNewAppy>:

''')


class MyDataTable(MDDataTable):
    pass

class MyNewAppy(FloatLayout):
    pass


class ExampleApp(MDApp):
    table = ObjectProperty(None)

    def build(self):
        return MyNewAppy()

    def on_start(self):
        self.table = MyDataTable(
                            pos_hint = {'center': (0.5, 0.5)},
                            size_hint = (0.9, 0.6),
                            check = True,
                            rows_num = 10,
                            column_data = [("File", dp(30)),
                                         ("Lines", dp(15)),
                                         ("Mean", dp(40)),
                                         ("Median", dp(30))],
                            row_data = [("lines0.jpg", 1, 153.411081973582, 170.0),
                                        ("lines0.jpg", 2, 155.4948937908497, 170.0),
                                        ("lines0.jpg", 3, 153.66490322580646, 171.0)],)
        self.table.open()


ExampleApp().run()