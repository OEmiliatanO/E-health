print("fuck")
from kivy.app import App
from kivy.lang import Builder


kv = Builder.load_string("""
Screen:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Setting Screen'
        Button:
            text: 'Exit'
            on_release: app.stop()
""")


class SettingScreen(App):

    def build(self):
        return kv


if __name__ == "__main__":
    print("hello")
    SettingScreen().run()
print("yo")