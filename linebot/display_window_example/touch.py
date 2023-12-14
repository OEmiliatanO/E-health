from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
import subprocess

Builder.load_string("""
<Screen>:
    btn:btn
    orientation: 'vertical'
    Label:
        id: msg
        text: "Hi"
        color: 1,0,0,1
        pos_hint: {"top":0.8}

    Button:
        id: btn
        size_hint: 0.2,0.2
        text: "Touch Me"
        on_release:  root.btn_touch_up()

""")

process = 0
class Screen(BoxLayout):
    btn = ObjectProperty(None)

    def btn_touch_up(self):
        global process
        process = subprocess.Popen(['python', 'C:\Programming\python\kivy_test\display_window_example\settings.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Touch Up ")


class TouchApp(App):
    def build(self):
        return Screen()


if __name__ == "__main__":
    cmd = ['python', 'settings.py']
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    TouchApp().run()