# reply_mail.py
import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.config import Config
Config.set('graphics','resizable', False)

class ReplyMailApp(App):
    def build(self):
        self.sender = self.get_sender_from_command_line()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Label to display the sender
        sender_label = Label(text=f"Send to: {self.sender}", size_hint_y=None, height=40)
        layout.add_widget(sender_label)

        # TextInput for the user to input the reply
        reply_input = TextInput(hint_text='Type your reply here', multiline=True, size_hint_y=None, height=300)
        layout.add_widget(reply_input)

        # Buttons for sending or canceling the reply
        send_button = Button(text='Send', on_release=lambda x: self.send_reply(reply_input.text), size_hint=(.2, None), background_color=(0.244, 0.811, 0.242, 1), top=1)
        cancel_button = Button(text='Cancel', on_release=lambda x: self.cancel_reply(), size_hint=(.2, None), background_color=(0.976, 0.176, 0.176, 1))

        button_layout = BoxLayout(spacing=5)  # Adjust the spacing as needed
        button_layout.add_widget(send_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)

        return layout

    def get_sender_from_command_line(self):
        # Extract the sender from the command line arguments
        if len(sys.argv) > 1:
            return sys.argv[1]
        return "Unknown Sender"

    def send_reply(self, reply_text):
        print(reply_text)
        # If the user presses send, terminate the app and return the reply text
        self.stop(reply_text)

    def cancel_reply(self):
        # If the user presses cancel, terminate the app and return nothing
        self.stop(None)


if __name__ == '__main__':
    Window.size = (500, 400)  # Set the initial size of the window
    Window.resizable = False  # Make the window non-resizable
    ReplyMailApp().run()
