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
    propose = ""
    original_input = ""
    def build(self):
        self.propose = self.get_propose_from_command_line()
        self.original_input = self.get_original_from_command_line()
        
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        # Label to display the propose
        propose_label = Label(text=f"Attach: {self.propose}", size_hint_y=None, height=40)
        layout.add_widget(propose_label)

        # TextInput for the user to input the reply
        reply_input = None
        if(self.original_input == ""):
            reply_input = TextInput(hint_text=f'Type {self.propose}', multiline=True, size_hint_y=None, height=300)
        else:
            reply_input = TextInput(text=self.original_input, multiline=True, size_hint_y=None, height=300)
        layout.add_widget(reply_input)

        # Buttons for sending or canceling the reply
        send_button = Button(text='OK', on_release=lambda x: self.send_reply(reply_input.text), size_hint=(.2, None), background_color=(0.244, 0.811, 0.242, 1), top=1)
        cancel_button = Button(text='Cancel', on_release=lambda x: self.cancel_reply(), size_hint=(.2, None), background_color=(0.976, 0.176, 0.176, 1))

        button_layout = BoxLayout(spacing=5)  # Adjust the spacing as needed
        button_layout.add_widget(send_button)
        button_layout.add_widget(cancel_button)
        layout.add_widget(button_layout)

        return layout

    def get_propose_from_command_line(self):
        # Extract the propose from the command line arguments
        if len(sys.argv) > 1:
            return sys.argv[1]
        return "Unknown Propose!?"
    
    def get_original_from_command_line(self):
        if len(sys.argv) > 2:
            return sys.argv[2]
        return ""
    
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
