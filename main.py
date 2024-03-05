from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
import os
from transformers import pipeline
from PIL import Image as PILImage
import shutil
import sqlite3
from kivy.uix.spinner import Spinner

classifier = pipeline("image-classification", model="Falcom/animal-classifier")
images_loc = []


def get_image(directory):
    images = []

    for i, j, k in os.walk(directory):
        for l in k:
            images.append(os.path.join(i, l))

    return images


class AnimalClassifierApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Top bar layout
        self.top_bar_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=50)


        conn = sqlite3.connect('69.db')
        cursor = conn.cursor()

        # Query the database to fetch values for the dropdown
        cursor.execute("SELECT path FROM selected_path")
        rows = cursor.fetchall()
        dropdown_values = [row[0] for row in rows]

        # Close the database connection
        conn.close()

        # Create a Spinner with values from the database
        self.spinner = Spinner(text='Select Option', values=dropdown_values, size_hint=(None, None), size=(100, 44))

        # Bind the on_text event to a function
        self.spinner.bind(on_text=self.on_search)

        self.layout.add_widget(self.spinner)
        # self.top_bar_layout.add_widget(self.folder_select_layout)

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

    def on_search(self, instance):
        images_loc.clear()
        # Retrieve the value from the search bar
        search_value = self.search_input.text
        dir_value = self.spinner.text
        for i in get_image(dir_value):

            image = PILImage.open(i).convert("RGB")
            result = classifier([image])
            label = max(result[0], key=lambda x: x['score'])
            if label['label'] == search_value:
                file_name = os.path.basename(i)
                print(f"The filename is {file_name}")
                images_loc.append(i)
        print(images_loc)

        for image_path in images_loc:
            img = KivyImage(source=image_path)
            self.layout.add_widget(img)


AnimalClassifierApp().run()