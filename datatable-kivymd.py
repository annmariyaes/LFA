from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.button import Button
from kivymd.uix.screen import MDScreen
from kivymd.uix.datatables import MDDataTable



class Example(MDApp):

    def build(self):
        self.i = 0
        self.rowData = ["Row. No."]
        self.button = Button(text="AddRow", size_hint_y=None, pos_hint={"bottom": 0})
        self.button.bind(texture_size=self.button.setter('size'))
        self.data_tables = None
        self.set_table(self.rowData)

    def set_table(self, data):
        if self.data_tables:
            self.data_tables.ids.container.remove_widget(self.button)

        self.data_tables = MDDataTable(size_hint=(0.9, 0.6), use_pagination=True, check=True,
                                       column_data=[("No.", dp(30))], row_data=[self.rowData])

        self.data_tables.ids.container.add_widget(self.button)
        screen = MDScreen()
        screen.add_widget(self.data_tables)
        return screen

    def on_start(self):
        self.button.bind(on_press=lambda x: self.addrow())

    def addrow(self):
        self.data_tables.dismiss(animation=False)
        self.i += 1
        self.set_table(self.rowData.append("Row {}".format(self.i)))


if __name__ == '__main__':
    Example().run()