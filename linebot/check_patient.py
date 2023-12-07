import sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout

# exm_tex = """0001
# Jager
# 01/01/2000,01:24:00
# 11/30/2023,08:04:09
# 3
# 11/30/2023,08:04:09
# 8
# BMI 0.000383673
# blood_sugar(mg/dL) 100.0
# body_fat_percentage 15.0
# estradiol(pg/mL) 10.2
# heart_rate(bpm) 65.0
# height(m) 1.88
# testosterone(ng/mL) 5.5
# weight(kg) 70.0
# [__START__]
# All numerical reports are in normal range.
# [__END__]
# [__START__]
# A normal person.
# [__END__]
# [__START__]
# Vitamin D tablet(10);calcium tablet(10);
# [__END__]
# jfalk;sfjk;dasjkfaj;,08:04:09
# 8
# BMI 0.000383673
# blood_sugar(mg/dL) 100.0
# body_fat_percentage 15.0
# estradiol(pg/mL) 10.2
# heart_rate(bpm) 65.0
# height(m) 1.88
# testosterone(ng/mL) 5.5
# weight(kg) 70.0
# [__START__]
# All numerical reports are in normal range.
# [__END__]
# [__START__]
# A normal person.
# [__END__]
# [__START__]
# Vitamin D tablet(10);calcium tablet(10);
# [__END__]
# 11/30/2023,08:04:09
# 8
# BMI 0.000383673
# blood_sugar(mg/dL) 100.0
# body_fat_percentage 15.0
# estradiol(pg/mL) 10.2
# heart_rate(bpm) 65.0
# height(m) 1.88
# testosterone(ng/mL) 5.5
# weight(kg) 70.0
# [__START__]
# All numerical reports are in normal range.
# [__END__]
# [__START__]
# A normal person.
# [__END__]
# [__START__]
# Vitamin D tablet(10);calcium tablet(10);
# [__END__]
# """


def process_input(text):
    try:
        id_now_line = 0
        lines = text.split('\n')
        names = ["UID", "name", "birth_date", "last_update_time"]
        
        answer = []
        now_str = ""
        for i in range(4):
            now_str+=names[i]+" : "+lines[i] +"\n"
        answer.append(now_str)
        
        N = int(lines[4])
        n = 0
        id_now_line = 4
        while(n<N):
            n_end = 0
            this_str = ""
            
            id_now_line+=1
            while(lines[id_now_line] == ""):
                id_now_line+=1
            this_str += "Date: "+lines[id_now_line]+"\n" + "----\n"
            
            id_now_line+=1
            M = int(lines[id_now_line])
            
            for smalln in range(M):
                id_now_line += 1
                temp_str = lines[id_now_line].split()
                this_str += temp_str[0] + ": " + temp_str[1] + "\n"
            
            
            while(1):
                id_now_line += 1
                if(lines[id_now_line] == "[__START__]"):
                    if(n_end == 0):
                        this_str += "\n------------------------------\nLab reports:\n"
                    if(n_end == 1):
                        this_str += "------------------------------\nDiagnosis:\n"
                    if(n_end == 2):
                        this_str += "------------------------------\nPrescription Note:\n"
                elif(lines[id_now_line] == "[__END__]"):
                    n_end+=1
                    this_str += "\n"
                    if(n_end >= 3):
                        break
                    continue
                else:
                    this_str += lines[id_now_line] + "\n"
            answer.append(this_str)
            n+=1
        
        return answer
    except:
        return ["Invalid ID"]

class ScrollableLabel(ScrollView):
    def __init__(self, **kwargs):
        super(ScrollableLabel, self).__init__(**kwargs)
        self.label = Label(size_hint=(None, None), text_size=(self.width, None))
        self.label.bind(texture_size=self.label.setter('size'))
        self.add_widget(self.label)

class MyApp(App):
    processed_info = []
    now_line = 0
    page_text = ""
    current_page = 0

    def build(self, **kwargs):
        super(MyApp, self).__init__(**kwargs)
        Window.bind(on_request_close=self.on_request_close)

        self.processed_info = sys.argv[1]
        self.processed_info = process_input(self.processed_info)

        self.pages = len(self.processed_info)
        self.current_page = 0

        self.layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        self.scrollable_label = ScrollableLabel(size_hint=(1, 0.8), width=600)

        BOTTOM_layout = AnchorLayout(size_hint=(1, 0.2), x = self.layout.center_x)
        button_layout = BoxLayout(size_hint=(0.3, 0.6), spacing=30, orientation='horizontal')
        next_button = Button(text=">", on_press=self.next_page)
        prev_button = Button(text="<", on_press=self.prev_page)
        self.page_label = Label(text=self.get_page_text())

        # Bind the text property to the method that updates the page_label text
        self.display_page(self.current_page)

        button_layout.add_widget(prev_button)
        button_layout.add_widget(self.page_label)
        button_layout.add_widget(next_button)

        BOTTOM_layout.add_widget(button_layout)

        self.layout.add_widget(self.scrollable_label)
        self.layout.add_widget(BOTTOM_layout)

        return self.layout


    def display_page(self, page_index):
        self.page_label.text = self.get_page_text()
        if 0 <= page_index < self.pages:
            self.scrollable_label.label.text = self.processed_info[page_index]

    def next_page(self, instance):
        if self.current_page < self.pages - 1:
            self.current_page += 1
            self.display_page(self.current_page)

    def prev_page(self, instance):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page(self.current_page)

    def on_request_close(self, *args):
        # Handle the request to close the application window
        print("Window is closing")
        # You can add additional cleanup or confirmation logic here
        return False  # Returning True allows the window to close
    def get_page_text(self):
        return f"{self.current_page + 1}/{self.pages}"


if __name__ == '__main__':

    app = MyApp()
    # app.bind(on_request_close=app.on_request_close)

    app.run()
    
    
    # app.process_input(input_string)
    
    # print("ha")
    
