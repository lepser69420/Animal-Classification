from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
import os

class AnimalClassifierApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Top bar layout
        self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)

        # Folder select option
        self.folder_select_layout = BoxLayout(orientation='horizontal', spacing=10)
        folder_select_label = Label(text='Folder Path:', font_size=18)
        self.folder_select_layout.add_widget(folder_select_label)

        self.folder_path_label = Label(text='D:/', font_size=18)
        self.folder_select_layout.add_widget(self.folder_path_label)

        folder_select_button = Button(text='Select Folder', size_hint=(None, None), height=40)
        folder_select_button.bind(on_release=self.open_folder_chooser)
        self.folder_select_layout.add_widget(folder_select_button)

        self.top_bar_layout.add_widget(self.folder_select_layout)

        # Search bar
        self.search_input = TextInput(hint_text='Search', multiline=False, font_size=16)
        self.search_input.bind(on_text_validate=self.on_search)  # Bind to 'on_text_validate' event
        self.top_bar_layout.add_widget(self.search_input)



        self.layout.add_widget(self.top_bar_layout)

        # Main content area
        self.main_layout = BoxLayout(orientation='horizontal')
        self.image_scroll_view = BoxLayout(orientation='vertical')
        self.main_layout.add_widget(self.image_scroll_view)

        # Controls layout
        controls_layout = BoxLayout(orientation='vertical', size_hint=(0.3, 1), padding=10, spacing=10)

        # Detect button
        detect_button = Button(text='Detect', size_hint_y=None, height=40)
        detect_button.bind(on_press=self.on_search)
        controls_layout.add_widget(detect_button)

        self.main_layout.add_widget(controls_layout)

        self.layout.add_widget(self.main_layout)

        return self.layout

    def open_folder_chooser(self, instance):
        file_chooser = FileChooserListView(path="D:/", dirselect=True)
        file_chooser.bind(on_submit=self.update_folder_path)
        popup = Popup(title='Select Folder', content=file_chooser, size_hint=(None, None), size=(400, 400))
        popup.open()

    def update_folder_path(self, instance, selected_path, *args):
        folder_path = selected_path[0] if selected_path else ""
        dir = os.path.dirname(folder_path)
        # print("Selected folder path:", dir)  # Debugging print statement
        self.folder_path_label.text = str(dir)

    def on_search(self, instance):
        # Retrieve the value from the search bar
        search_value = self.search_input.text
        dir_value = self.folder_path_label.text
        # Perform search based on the input value
        # For simplicity, just displaying the search results in a popup
        popup_content = Label(text=f'Search results for: {search_value} {dir_value}')
        popup = Popup(title='Search Results', content=popup_content, size_hint=(None, None), size=(400, 400))
        popup.open()



if __name__ == '__main__':
    AnimalClassifierApp().run()
