from kivy.config import Config
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import Image

import sys

# Set the window size
Config.set('graphics', 'width', '650')
Config.set('graphics', 'height', '900')
Config.set('graphics', 'resizable', False)


class MailDisplay(ScrollView):
    def __init__(self, **kwargs):
        super(MailDisplay, self).__init__(**kwargs)

        # Extract command-line arguments
        time = sys.argv[1] if len(sys.argv) > 1 else "N/A"
        sender = sys.argv[2] if len(sys.argv) > 2 else "N/A"
        receiver = sys.argv[3] if len(sys.argv) > 3 else "N/A"
        content = sys.argv[4] if len(sys.argv) > 4 else "N/A"

        # Create a FloatLayout
        float_layout = FloatLayout()

        background_image = Image(source='mail_background2.jpg', allow_stretch=True, keep_ratio=False)
        float_layout.add_widget(background_image)
        
        # Display the mail information in rows
        labels = [
            f"Time : {time}",
            f"Sender : {sender}",
            f"Receiver : {receiver}",
            "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=",
        ]
        
        top_position = 930  # Initial top position
        font_size = 25  # Set your desired font size
        spacing = 0.05  # Adjust the spacing between texts

        for text1, in zip(labels):
            label1 = Label(
                text=text1,
                size_hint=(1, None),
                height=40,  # Adjust the height as needed
                font_size=font_size,
                y = top_position,
                # pos_hint={"top": top_position},
                halign='center',
                valign='top',
                width=70,
                # x = 50,
                color=(0, 0, 0, 1) 
            )
            
            float_layout.add_widget(label1)
            top_position -= (label1.height + spacing)
        
        top_position += 40
        max_content_width = 550
        lab_cont = Label(
            text=f"  {content}",
            size_hint=(1, None),
            height=40,  # Adjust the height as needed
            font_size=font_size,
            y = (top_position)/2,
            halign='center',
            valign='top',
            color=(0, 0, 0, 1),  # Black text color
            text_size=(max_content_width, None),
            width = max_content_width
        )
        float_layout.add_widget(lab_cont)

        # Set the content of the ScrollView to the FloatLayout
        self.add_widget(float_layout)

class MyApp(App):
    def build(self):
        return MailDisplay()

if __name__ == '__main__':
    MyApp().run()

