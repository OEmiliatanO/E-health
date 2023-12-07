from kivy.properties import StringProperty, ObjectProperty
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.textinput import TextInput
from kivy.base import runTouchApp
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

import os
import signal

import subprocess
from datetime import datetime

import random

import UIcode
import user as fish
import assistant_conversation as ASConv

#it will be modify later to correct path
from API import * 
from pinfo import med_record_t, patient_info_t

PAGE_NOW = 1
USER_NAME = ""

def process_input(text):
    id_now_line = 0
    # print("why:",id_now_line)
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
    print("here?")
    for n in range(N):
        print("or here?")
        n_end = 0
        this_str = ""
        
        id_now_line+=1
        this_str += "Date: "+lines[id_now_line]+"\n" + "----\n"
        
        id_now_line+=1
        print(id_now_line, 100)
        id_now_line = 6
        M = int(lines[id_now_line])
        
        for smalln in range(M):
            id_now_line += 1
            temp_str = lines[id_now_line].split()
            this_str += temp_str[0] + ": " + temp_str[1] + "\n"
        
        
        while(n_end < 3):
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
                continue
            else:
                this_str += lines[id_now_line] + "\n"
        answer.append(this_str)
        # n+=1
    id_now_line = 0
    return answer

def change_to_Reservatoin(obj, page_now = 1):
    global PAGE_NOW
    obj.clear_widgets()
    
    PAGE_NOW = page_now
    
    The_doctor_reservation = UIcode.browse_reservation(USER_NAME, pack=True, page_pack= 3) #取得預約陣列
    Reservation_layout.The_doctor_s_resv = The_doctor_reservation
    page_limit = len(The_doctor_reservation)
    
    Reservation_layout.page_limit = page_limit
    Reservation_layout.page_text = f'{PAGE_NOW}/{page_limit}'

    try:
        Reservation_layout.reservation_text1 = ("Date :                     " + str(The_doctor_reservation[PAGE_NOW-1][0].time) +
                                                "\nPatient name :    " + str(The_doctor_reservation[PAGE_NOW-1][0].patient.name) + 
                                                "\nNumber :              " + str(The_doctor_reservation[PAGE_NOW-1][0].number) + 
                                                "\nNote :                    " + str(The_doctor_reservation[PAGE_NOW-1][0].note))
    except:
        Reservation_layout.reservation_text1 = "-"

    try:
        Reservation_layout.reservation_text2 = (
            "Date :                     " + str(The_doctor_reservation[PAGE_NOW-1][1].time) +
            "\nPatient name :    " + str(The_doctor_reservation[PAGE_NOW-1][1].patient.name) + 
            "\nNumber :              " + str(The_doctor_reservation[PAGE_NOW-1][1].number) + 
            "\nNote :                    " + str(The_doctor_reservation[PAGE_NOW-1][1].note)
        )
    except:
        Reservation_layout.reservation_text2 = "-"

    try:
        Reservation_layout.reservation_text3 = (
            "Date :                     " + str(The_doctor_reservation[PAGE_NOW-1][2].time) +
            "\nPatient name :    " + str(The_doctor_reservation[PAGE_NOW-1][2].patient.name) + 
            "\nNumber :              " + str(The_doctor_reservation[PAGE_NOW-1][2].number) + 
            "\nNote :                    " + str(The_doctor_reservation[PAGE_NOW-1][2].note)
        )
    except:
        Reservation_layout.reservation_text3 = "-"
    
    cur_widget = Factory.Reservation_layout()
    obj.add_widget(cur_widget)

def change_to_Chat(obj, page_now = 1): #
    global PAGE_NOW
    obj.clear_widgets()

    The_doctor_chat = UIcode.browse_chat(USER_NAME, pack=True, page_pack= 3) #取得預約陣列
    Chat_layout.The_doctor_s_chat = The_doctor_chat
    page_limit = len(The_doctor_chat)
    PAGE_NOW = page_now
    
    Chat_layout.page_limit = page_limit
    Chat_layout.page_text = f'{PAGE_NOW}/{page_limit}'

    try:
        mail = The_doctor_chat[PAGE_NOW-1][0]
        content = ""
        if len(mail.content) > 20:
            content = ''.join(mail.content[:20]) + '...'
        else:
            content = ''.join(mail.content)
        content = content.replace('\n', '')
        Chat_layout.chat_text1 = (
            "Date :           " + str(The_doctor_chat[PAGE_NOW-1][0].time) +
            "\nSender :      " + str(The_doctor_chat[PAGE_NOW-1][0].sender.name) + 
            "\nRecipient :  " + str(The_doctor_chat[PAGE_NOW-1][0].recipient.name) + 
            "\nContent :     " + str(content))
    except:
        Chat_layout.chat_text1 = "-"

    try:
        mail = The_doctor_chat[PAGE_NOW-1][1]
        content = ""
        if len(mail.content) > 20:
            content = ''.join(mail.content[:20]) + '...'
        else:
            content = ''.join(mail.content)
        content = content.replace('\n', '')
        Chat_layout.chat_text2 = (
            "Date :           " + str(The_doctor_chat[PAGE_NOW-1][1].time) +
            "\nSender :      " + str(The_doctor_chat[PAGE_NOW-1][1].sender.name) + 
            "\nRecipient :  " + str(The_doctor_chat[PAGE_NOW-1][1].recipient.name) + 
            "\nContent :     " + str(content)
        )
    except:
        Chat_layout.chat_text2 = "-"

    try:
        mail = The_doctor_chat[PAGE_NOW-1][2]
        content = ""
        if len(mail.content) > 20:
            content = ''.join(mail.content[:20]) + '...'
        else:
            content = ''.join(mail.content)
        content = content.replace('\n', '')
        Chat_layout.chat_text3 = (
            "Date :           " + str(The_doctor_chat[PAGE_NOW-1][2].time) +
            "\nSender :      " + str(The_doctor_chat[PAGE_NOW-1][2].sender.name) + 
            "\nRecipient :  " + str(The_doctor_chat[PAGE_NOW-1][2].recipient.name) + 
            "\nContent :     " + str(content)
        )
    except:
        Chat_layout.chat_text3 = "-"
  
    # for i in range(3): Chat_layout.chat_color_list[i] = ( 0.522, 0.702, 0.875 )
    cur_widget = Factory.Chat_layout()
    obj.add_widget(cur_widget)

def change_to_Prescribe(obj): #
    obj.clear_widgets()
    PAGE_NOW = 1
    current_datetime = datetime.now()
    Prescribe_layout.date = current_datetime.strftime("%m/%d/%Y,%H:%M:%S")
    Prescribe_layout.save_date = current_datetime
    cur_widget = Factory.Prescribe_layout()
    obj.add_widget(cur_widget)

def change_to_Search(obj): #
    obj.clear_widgets()
    cur_widget = Factory.Patient_info_layout()
    PAGE_NOW = 1
    obj.add_widget(cur_widget)

def change_to_main(obj):
    global PAGE_NOW
    obj.clear_widgets()
    PAGE_NOW = 1
    cur_widget = Factory.MainWidget()
    obj.add_widget(cur_widget)

# process = None
# def display_info(info_tex):
#     try:
#         cmd = ['python', 'check_patient.py', info_tex]
        
#         global process
#         process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
#     except Exception as e:
#         print("display info Error:", str(e))

class Prescribe_layout(BoxLayout):
    scroll_tex = StringProperty("")
    key_dict = {}
    
    date = StringProperty("testdate")
    save_date = None
    
    prompt = StringProperty("")
    
    temp_lab = ""
    temp_diag = ""
    temp_presc = ""
    
    temp_name =""
    temp_birthday = ""
    
    def build(self):
        pass
    
    def open_lab_report_editor(self):
        try:
            print(self.temp_lab)
            cmd = ['python', 'edit_info.py', "Lab Report", self.temp_lab]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Edit from edit_info.py:", reply_text)
                    self.temp_lab = reply_text
                else:
                    print("User canceled the edit.")
            else:
                print("Error:", result.stderr)
        except Exception as e:
            print("Error:", str(e))
    
    def open_diagnosis_editor(self):
        try:
            cmd = ['python', 'edit_info.py', "Diagnosis", self.temp_diag]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Edit from edit_info.py:", reply_text)
                    self.temp_diag = reply_text
                else:
                    print("User canceled the edit.")
            else:
                print("Error:", result.stderr)
        except Exception as e:
            print("Error:", str(e))

    def open_prescribe_editor(self):
        try:
            cmd = ['python', 'edit_info.py', "Prescribe", self.temp_presc]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Edit from edit_info.py:", reply_text)
                    self.temp_presc= reply_text
                else:
                    print("User canceled the edit.")
            else:
                print("Error:", result.stderr)
        except Exception as e:
            print("Error:", str(e))

    def open_info_creator(self, patient_uid):
        try:
            cmd = ['python', 'create_info.py', patient_uid]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Edit from create_info.py:", reply_text)
                    self.temp_name, self.temp_birthday= reply_text.split(' ')
                else:
                    print("User canceled create.")
            else:
                print("Error:", result.stderr)
        except Exception as e:
            print("Error:", str(e))
  
    def update_scrollview(self):
        tex = self.ids.prescribe_key_input.text
        proccessing = tex.split('\n')
        new_scorll_tex = ""
        nowid = 1
        for i in proccessing:
            try:
                key, value = i.split(" ")
                new_scorll_tex += str(nowid) + ". " + key + " : " + value + "\n"
                nowid+=1
            except:
                continue
        self.scroll_tex = new_scorll_tex
        self.update_dict
    
    def update_dict(self):
        tex = self.ids.prescribe_key_input.text
        proccessing = tex.split('\n')
        temp_dict = {}
        for i in proccessing:
            try:
                key, value = i.split(" ")
                temp_dict[key] = value
            except:
                continue
        self.key_dict = temp_dict
    
    def finish(self):
        try:
            patient_uid = self.ids.prescribe_patient_uid_input.text
            if(patient_uid == ""):
                print("inputext error")
                self.prompt = "Inputext eroor"
                return
        except:
            print("inputext error")
            self.prompt = "Iinputext eroor"
            return
        try:
            patient_now = UIcode.get_patients_info_by_id(patient_uid)
        except:
            try:
                print("patient load error")
                self.prompt = "Invalid UID"
                self.open_info_creator(patient_uid)
                self.temp_birthday_tuple = datetime.strptime(self.temp_birthday, '%m/%d/%Y,%H:%M:%S')
                self.temp_birthday_tuple = self.temp_birthday_tuple.timetuple()
                patient_now = pinfo.patient_info_t(UID=patient_uid, name=self.temp_name, birth_date=self.temp_birthday_tuple)
            except:
                return
        try:
            self.update_dict()
            report_now = pinfo.reports_t(image_records=[], numerical_records=self.key_dict, lab_report=self.temp_lab, diagnosis=self.temp_diag, prescription=self.temp_presc)
            med_now = pinfo.med_record_t(self.save_date.timetuple(), report_now)
            patient_now.med_records.append(med_now)
            patient_now.last_update_time = self.save_date.timetuple()
        except:
            print("data processing error")
            self.prompt = "Data processing error"
            return
        # try:
        UIcode.create_patients_info_by_id(patient_uid, patient_now)
        # except Exception as e:
        #     print("data saving error")
        #     print("Error:", str(e))
        #     self.prompt = "Data saving error"
        #     return
        self.prompt = f"Saved: {patient_uid}\nSuccessful!"
        
    def chg_widget_main(self):
        change_to_main(self)
    def chg_widget_search(self):
        """
        Change to Search
        """
        change_to_Search(self)    
    def chg_widget_reservation(self):
        """
        Change to Reservation
        """
        change_to_Reservatoin(self)   
    def chg_widget_chat(self):
        """
        Change to Chat
        """
        change_to_Chat(self)      
    def chg_widget_prescribe(self):
        """
        Change to Prescribe
        """
        change_to_Prescribe(self)


class Patient_info_layout(BoxLayout):
    page_limit = 0

    process = None #check proc
    check_process = None #reply proc

    def get_info_by_id(self):
        info = None
        try:
            id = self.ids.input_patient_uid.text
            info = UIcode.get_patients_info_by_id(id)
        except:
            info = "sorry, cannot find this patient"
        return str(info)
    
    def display_info(self):
        tex = self.get_info_by_id()
        # print("why:",str(tex))
        result = None
        try:
            cmd = ['python', 'check_patient.py', tex]

            # Use subprocess.run to wait for the child process to finish
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Reply from reply_mail.py:", reply_text)
                else:
                    print("User canceled the reply.")
            else:
                print("Error:", result.stderr)
        except Exception as e:
            print("Error:", str(e))

    def chg_widget_main(self):
        change_to_main(self)
    def chg_widget_search(self):
        """
        Change to Search
        """
        change_to_Search(self)    
    def chg_widget_reservation(self):
        """
        Change to Reservation
        """
        change_to_Reservatoin(self)   
    def chg_widget_chat(self):
        """
        Change to Chat
        """
        change_to_Chat(self)      
    def chg_widget_prescribe(self):
        """
        Change to Prescribe
        """
        change_to_Prescribe(self)

#Chat Layout
class Chat_layout(BoxLayout):
    
    The_doctor_s_chat = []
    
    page_limit = 0
    
    page_text = StringProperty(f'{PAGE_NOW}/{page_limit}')
    doctor_name = StringProperty('')
    
    chat_text1 = StringProperty("1")
    chat_text2 = StringProperty("2")
    chat_text3 = StringProperty("3")
     
    process = None #check proc
    reply_process = None #reply proc
    
    def check_mail(self, id):
        try:
            now_id = int(id)
            mail = self.The_doctor_s_chat[PAGE_NOW-1][now_id-1]
            time = mail.time
            sender = mail.sender.name
            receiver = mail.recipient.name
            content = mail.content


            cmd = ['python', 'check_mail.py', time, sender, receiver, content]
            
            self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
        except Exception as e:
            print("Error:", str(e))

    def delete_mail(self, id):
        try:
            that_mail = self.The_doctor_s_chat[PAGE_NOW-1][id-1]
            UIcode.delete_chat(that_mail)
            self.fix_page()
        except:
            return
  
    def reply_mail(self, id):
        try:
            now_id = int(id)
            mail = self.The_doctor_s_chat[PAGE_NOW-1][now_id-1]
            sender = mail.sender.name

            cmd = ['python', 'reply_mail.py', sender]

            # Use subprocess.run to wait for the child process to finish
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                reply_text = result.stdout.strip()
                if reply_text:
                    print("Reply from reply_mail.py:", reply_text)
                    mail.reply(reply_text)
                else:
                    print("User canceled the reply.")
            else:
                print("Error:", result.stderr)

        except Exception as e:
            print("Error:", str(e))

    def next_page(self):
        """
        change to next page, not working if it reach limit
        """
        global PAGE_NOW
        if(PAGE_NOW >= self.page_limit): return
        
        change_to_Chat(self, PAGE_NOW+1)

    def prev_page(self):
        """
        change to next page, not working if it above 1
        """
        if(PAGE_NOW <= 1): return
        
        change_to_Chat(self, PAGE_NOW-1)
    
    def fix_page(self):
        global PAGE_NOW
        self.page_limit = len(UIcode.browse_chat(USER_NAME, pack=True, page_pack= 3))
        while( PAGE_NOW > self.page_limit ): PAGE_NOW -= 1
        while( PAGE_NOW < 1 ): PAGE_NOW += 1
        change_to_Chat(self, PAGE_NOW)

    def chg_widget_main(self):
        change_to_main(self)
    def chg_widget_search(self):
        """
        Change to Search
        """
        change_to_Search(self)    
    def chg_widget_reservation(self):
        """
        Change to Reservation
        """
        change_to_Reservatoin(self)   
    def chg_widget_chat(self):
        """
        Change to Chat
        """
        change_to_Chat(self)      
    def chg_widget_prescribe(self):
        """
        Change to Prescribe
        """
        change_to_Prescribe(self)
        
class WidgetsExample(GridLayout):
    # def __init__(self, **kwargs):
    #     super().__init__(**kwargs)
    #     b1 = Button(text = 'A')
    #     b2 = Button(text = 'B')
    #     self.add_widget(b1)
    #     self.add_widget(b2)
    def ret(self):
        change_to_main(self)
        pass

class Reservation_layout(BoxLayout):
    
    The_doctor_s_resv = []
    
    page_limit = 0
    
    page_text = StringProperty(f'{PAGE_NOW}/{page_limit}')
    doctor_name = StringProperty('')
    
    reservation_text1 = StringProperty("1")
    reservation_text2 = StringProperty("2")
    reservation_text3 = StringProperty("3")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
    def next_page(self):
        """
        change to next page, not working if it reach limit
        """
        global PAGE_NOW
        if(PAGE_NOW >= self.page_limit): return
        
        change_to_Reservatoin(self, PAGE_NOW+1)

    def prev_page(self):
        """
        change to next page, not working if it above 1
        """
        if(PAGE_NOW <= 1): return
        
        change_to_Reservatoin(self, PAGE_NOW-1)
    
    def fix_page(self):
        global PAGE_NOW
        self.page_limit = len(UIcode.browse_reservation(USER_NAME, pack=True, page_pack= 3))
        while( PAGE_NOW > self.page_limit ): PAGE_NOW -= 1
        while( PAGE_NOW < 1 ): PAGE_NOW += 1
        change_to_Reservatoin(self, PAGE_NOW)
    
    def delete_resv(self, id):
        now_id = int(id)
        try:
            now_obj = self.The_doctor_s_resv[PAGE_NOW-1][now_id-1]
            UIcode.delete_reservation(now_obj)
            self.fix_page()
        except:
            return
    def chg_edit_resv(self,id):
        try:
            now_id = int(id)
            EditResv.patient_name = "Name:  " + str(self.The_doctor_s_resv[PAGE_NOW-1][now_id-1].patient.name)
            EditResv.patient_number = self.The_doctor_s_resv[PAGE_NOW-1][now_id-1].number
            
            year, month, day = self.The_doctor_s_resv[PAGE_NOW-1][now_id-1].time.split("-")
            EditResv.patient_time_y = year
            EditResv.patient_time_m = month
            EditResv.patient_time_d = day
            
            EditResv.patient_note = self.The_doctor_s_resv[PAGE_NOW-1][now_id-1].note
            
            EditResv.old_obj = self.The_doctor_s_resv[PAGE_NOW-1][now_id-1]
            
            self.clear_widgets()
            cur_widget = Factory.EditResv()
            self.add_widget(cur_widget)
        except:
            return

    def chg_widget_main(self):
        change_to_main(self)
    def chg_widget_search(self):
        """
        Change to Search
        """
        change_to_Search(self)    
    def chg_widget_reservation(self):
        """
        Change to Reservation
        """
        change_to_Reservatoin(self)   
    def chg_widget_chat(self):
        """
        Change to Chat
        """
        change_to_Chat(self)      
    def chg_widget_prescribe(self):
        """
        Change to Prescribe
        """
        change_to_Prescribe(self)

class EditResv(BoxLayout):
    patient_name = "who care?"
    patient_number = 0
    patient_time_y = '2023'
    patient_time_m = '12'
    patient_time_d = '02'
    patient_note = "fucknows"
    old_obj = None
    def cancel(self):
        change_to_Reservatoin(self,page_now=PAGE_NOW)
    def save(self):
        d = self.ids.input_time_d.text
        m = self.ids.input_time_m.text
        y = self.ids.input_time_y.text
        date = str(y) + "-" + str(m) + "-" + str(d)
        
        num = int(self.ids.input_number.text)
        note = str(self.ids.input_note.text)
        
        UIcode.edit_reservation(self.old_obj, date, num, note)
        
        change_to_Reservatoin(self,page_now=PAGE_NOW)

class EditResvApp(App):
    def build(self):
        return EditResv()

class MainWidget(BoxLayout):
    doctor_id_str = ""
    doctor_id = StringProperty("")
    conversation = StringProperty("")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conversation = ASConv.hello_conv(self.doctor_id_str)
    
    def talk(self):
        self.conversation = ASConv.daily_conversation_to_doctor(self.doctor_id_str)
    
    def chg_widget_search(self):
        """
        Change to Search
        """
        change_to_Search(self)       
    def chg_widget_reservation(self):
        """
        Change to Reservation
        """
        change_to_Reservatoin(self)     
    def chg_widget_chat(self):
        """
        Change to Chat
        """
        change_to_Chat(self)
    def chg_widget_prescribe(self):
        """
        Change to Prescribe
        """
        change_to_Prescribe(self)

class LoginWidget(BoxLayout):
    message_text = StringProperty("")
    def login(self):
        user_name = self.ids.input_user_name.text
        password = self.ids.input_password.text

        # Now you have the values of user_name and password
        print("Line ID:", user_name)
        print("Password:", password)
        boolll = UIcode.Doctor_login(user_name, password)
        if(boolll):
            global USER_NAME
            MainWidget.doctor_id = user_name
            MainWidget.doctor_id_str = str(user_name)
            USER_NAME = user_name
            self.clear_widgets()
            cur_widget = Factory.MainWidget()
            self.add_widget(cur_widget)
        else:
            self.message_text = "Wrong password or line_id!"

class WindowManager(ScreenManager):
    pass

# kv = Builder.load_file("TheLab.kv")
class TheLabApp(App):
    # def build(self):
    #     return kv
    pass

if(__name__ == '__main__'):
    UIcode.json_initiallized()
    UIcode.add_test()
    TheLabApp().run()