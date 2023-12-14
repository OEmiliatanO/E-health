import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.config import Config
import re


Config.set('graphics', 'resizable', False)

class ReplyMailApp(App):
    uid = ""
    original_input = ""
    
    def build(self):
        self.uid = self.get_uid_from_command_line()
        self.original_input = self.get_original_from_command_line()

        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Label to display the uid
        uid_label = Label(text=f"Create: {self.uid}", size_hint_y=None, height=40)
        layout.add_widget(uid_label)

        # TextInput for the user's name
        name_input = TextInput(hint_text='Enter your name', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(name_input)

        # TextInput for the user's birthday
        birthday_input = TextInput(hint_text='Enter your birthday (MM/DD/YYYY,HH:MM:SS)', multiline=False, size_hint_y=None, height=40)
        layout.add_widget(birthday_input)

        # Buttons for sending or canceling the reply
        send_button = Button(text='OK', on_release=lambda x: self.send_reply(name_input.text, birthday_input.text), size_hint=(.2, None), background_color=(0.244, 0.811, 0.242, 1), top=1)
        cancel_button = Button(text='Cancel', on_release=lambda x: self.cancel_reply(), size_hint=(.2, None), background_color=(0.976, 0.176, 0.176, 1))

        button_layout = BoxLayout(spacing=5)  # Adjust the spacing as needed
        button_layout.add_widget(send_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)

        return layout

    def get_uid_from_command_line(self):
        # Extract the uid from the command line arguments
        if len(sys.argv) > 1:
            return sys.argv[1]
        return "Unknown[error!]"

    def get_original_from_command_line(self):
        if len(sys.argv) > 2:
            return sys.argv[2]
        return ""

    def send_reply(self, name, birthday):
        if self.is_valid_birthday(birthday):
            print(f"{name} {birthday}")
            # If the user presses send and the birthday is valid, terminate the app
            self.stop()
        else:
            # If the birthday is not valid, show an error popup
            self.show_error_popup("Invalid birthday format. Please use \nMM/DD/YYYY,HH:MM:SS")

    def cancel_reply(self):
        # If the user presses cancel, terminate the app
        self.stop()

    def is_valid_birthday(self,input_text):
        pattern = r'^\d{2}/\d{2}/\d{4},\d{2}:\d{2}:\d{2}$'
        return re.match(pattern, input_text) is not None

    def show_error_popup(self, message):
        # Show a popup with an error message
        content = BoxLayout(orientation='vertical', spacing=10)
        content.add_widget(Label(text=message))
        close_button = Button(text="Close", size_hint_y=None, height=40)
        popup = Popup(title='Error', content=content, size_hint=(None, None), size=(400, 200), auto_dismiss=False)
        content.add_widget(close_button)

        def close_popup(instance):
            popup.dismiss()

        close_button.bind(on_press=close_popup)
        popup.open()


if __name__ == '__main__':
    Window.size = (500, 400)  # Set the initial size of the window
    Window.resizable = False  # Make the window non-resizable
    ReplyMailApp().run()
