from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
import sqlite3
from kivy.uix.screenmanager import Screen, ScreenManager




class FolderSelectionPopup(Popup):
    def __init__(self, callback, **kwargs):
        super(FolderSelectionPopup, self).__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.title = "Select a Folder"
        self.file_chooser = FileChooserListView(filters=['.*'], path='.')
        self.callback = callback
        self.content = BoxLayout(orientation='horizontal')
        self.content.add_widget(self.file_chooser)

        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        select_button = Button(text='Select', size_hint_x=0.5)
        select_button.bind(on_press=self.select_folder)
        button_layout.add_widget(select_button)

        cancel_button = Button(text='Cancel', size_hint_x=0.5)
        cancel_button.bind(on_press=self.dismiss)
        button_layout.add_widget(cancel_button)

        self.content.add_widget(button_layout)

    def select_folder(self, instance):
        selected_folder = self.file_chooser.path
        if selected_folder:
            self.callback(selected_folder)
            self.dismiss()


class FolderSelectionApp(App):
    def build(self):

        self.selected_folders = str()
        self.fuck = []

        main_layout = BoxLayout(orientation='vertical')
        select_folder_button = Button(text="Select Folder")
        select_folder_button.bind(on_press=self.open_folder_selection)
        main_layout.add_widget(select_folder_button)

        conn = sqlite3.connect('69.db')
        cursor = conn.cursor()

        # Query the database to fetch values for the dropdown
        cursor.execute("SELECT path FROM selected_path")
        rows = cursor.fetchall()
        for i in rows:
            self.folder_label = Label(text=str(i[0]))
            main_layout.add_widget(self.folder_label)

        # Close the database connection
        conn.close()


        self.search_input = TextInput(hint_text='Search', multiline=False, font_size=16)
        self.search_input.bind(on_text_validate=self.on_search)  # Bind to 'on_text_validate' event
        main_layout.add_widget(self.search_input)

        detect_button = Button(text='Remove path', size_hint_y=None, height=40)
        detect_button.bind(on_press=self.on_search)
        main_layout.add_widget(detect_button)


        return main_layout

    def open_folder_selection(self, instance):
        folder_selection_popup = FolderSelectionPopup(callback=self.add_selected_folder)
        folder_selection_popup.open()

    def add_selected_folder(self, folder_path):
        self.selected_folders = folder_path
        # self.selected_folders.append(folder_path)
        self.update_selected_folders_label()

    def update_selected_folders_label(self):
        # Connect to the SQLite database
        conn = sqlite3.connect('69.db')
        cursor = conn.cursor()

        # Insert the variable data into the database
        cursor.execute("INSERT INTO selected_path (path) VALUES (?)", (self.selected_folders,))

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()

    def on_search(self, instance):
        search_value = self.search_input.text
        conn = sqlite3.connect('69.db')
        cursor = conn.cursor()

        # Check if the value exists in the database
        cursor.execute("SELECT path FROM selected_path WHERE path = ?", (search_value,))
        row = cursor.fetchone()

        if row is not None:
            # Delete the row
            cursor.execute("DELETE FROM selected_path WHERE path = ?", (search_value,))
            print(f"The path {search_value} has been deleted from the database.")
        else:
            print(f"The path {search_value} is not present in the database.")

        # Commit the changes
        conn.commit()

        # Close the connection
        conn.close()


if __name__ == '__main__':
    FolderSelectionApp().run()
