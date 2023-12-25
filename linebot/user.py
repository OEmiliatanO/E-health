import json, os
import sys
from datetime import datetime, timedelta
from time import sleep

try:
    from ..include.API import *
    from ..include.pinfo import med_record_t, patient_info_t
except ImportError:
    sys.path.append(os.path.expanduser("~/ehealth/include"))
    from API import *
    from pinfo import med_record_t, patient_info_t

class UserNotFoundException(Exception):
    "Raised when target user not found"
    pass

class User:
    allUsers = [] # 儲存所有的 User
    def __init__(self, line_userid, permission, information=None): # init
        if line_userid==None:
            raise ValueError("line_userid cannot be None")
        if permission==None:
            raise ValueError("permission cannot be None")
        self.line_userid = line_userid
        self.information = information
        self.permission = permission
        self.password = None

    def setPassword(self, password): # 設定密碼，只有 Doctor 需要輸入密碼
        self.password = password

    def getLoginState(self, password): # 確認密碼有沒有對
        try:
            if password == None or password == self.password:
                return True
            else:
                return False
        except:
            return False
        
    def appendUser(self): # 把自己加入allUser裡面，用Doctor跟Patient時會自己做
        self.allUsers.append(self)
    
    @staticmethod
    def toJson(path=os.path.expanduser("~/ehealth/linebot/data/users.json")): # 把 User 打包成Json
        with open(path, 'w') as file:
            json.dump([vars(user) for user in User.allUsers], file, indent=2)
    
    @staticmethod
    def loadJson(path=os.path.expanduser("~/ehealth/linebot/data/users.json")): # 把Json 轉入 allUsers
        User.allUsers.clear()
        with open(path, 'r') as file:
            data = json.load(file)
            for user_data in data:
                user_type = user_data.pop('permission', None)
                if user_type == 'doctor':
                    Doctor(**user_data)
                elif user_type == 'patient':
                    Patient(**user_data)
                else:
                    raise ValueError(f"Unknown user type: {user_type}")
        return User.allUsers

class Doctor(User): # 需要密碼，其他身分資訊不需要
    def __init__(self, name, line_userid, password, information=None):
        super().__init__(line_userid, permission="doctor", information=information)
        self.setPassword(password)
        self.name = name
        self.appendUser()

    @staticmethod
    def getAllDoctor():
        allDoctor = []
        for user in User.allUsers:
            if user.permission == "doctor":
                allDoctor.append(user)
        return allDoctor

class Patient(User): # 不需要密碼，但需要身分資訊
    def __init__(self, name, birth_date, id_number, phone, blood_type=None, emergency_contact=None,
                 emergency_contact_phone=None, email=None, height=None, weight=None,
                 medical_history=None, notes=None, line_userid=None, information=None, *args, **kw):
        if name is None or birth_date is None or id_number is None or phone is None:
            raise ValueError("Name, birth_date, id_number, phone, and line_userid cannot be None.")
        super().__init__(line_userid, permission="patient", information=information)
        self.name = name
        self.birth_date = birth_date
        self.id_number = id_number
        self.phone = phone
        self.blood_type = blood_type
        self.emergency_contact = emergency_contact
        self.emergency_contact_phone = emergency_contact_phone
        self.email = email
        self.height = height
        self.weight = weight
        self.medical_history = medical_history
        self.notes = notes
        self.appendUser()

    def getInfo(self, path=os.path.expanduser("~/ehealth/DB/central_DB")) -> patient_info_t:
        api = DB_API()
        api.set_DB(DB_factory.create(DB_factory.plain_text_DB), path)
        info = api.load_info(self.id_number)
        return info
    
    def createInfo(self, pinfo, path=os.path.expanduser("~/ehealth/DB/central_DB")) -> None:
        api = DB_API()
        api.set_DB(DB_factory.create(DB_factory.plain_text_DB), path)
        api.write_back(self.id_number, pinfo)

    def detectLab(self, exe_file=os.path.expanduser("~/ehealth/call_lab.elf"), dignose_file=os.path.expanduser("~/ehealth/DB/diagnose/")):
        cmd = exe_file+" "+dignose_file+self.id_number+".info"+" "+self.id_number
        os.system(cmd)
        sleep(0.1)
        result_dict = {}
        with open(dignose_file, 'r') as file:
            lines = file.readlines()
            current_key = None
            current_value = ""

            for line in lines:
                line = line.strip()
                if line.endswith(":"):
                    current_key = line[:-1].lower().replace(" ", "_") 
                else:
                    current_value += line + " "
            result_dict[current_key] = current_value.strip()
        return result_dict

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Birth Date: {self.birth_date}")
        print(f"ID Number: {self.id_number}")
        print(f"Phone: {self.phone}")
        print(f"Blood Type: {self.blood_type}")
        print(f"Emergency Contact: {self.emergency_contact}")
        print(f"Emergency Contact Phone: {self.emergency_contact_phone}")
        print(f"Email: {self.email}")
        print(f"Height: {self.height}")
        print(f"Weight: {self.weight}")
        print(f"Medical History: {self.medical_history}")
        print(f"Notes: {self.notes}")

class Message: 
    allMessage = [] # 儲存所有現有的Message物件
    def __init__(self, recipient:Doctor, sender:Patient, content, time=None):
        self.time = datetime.now().strftime("%Y-%m-%d %H:%M:%S") if time==None else time
        self.content = content
        if type(sender) == type(str()):
            for user in User.allUsers:
                if user.line_userid == sender:
                    self.sender = user
        elif isinstance(sender, User):
            self.sender = sender
        else:
            raise TypeError("Wrong Type")
        if type(recipient) == type(str()):
            for user in User.allUsers:
                if user.line_userid == recipient:
                    self.recipient = user
        elif isinstance(recipient, User):
            self.recipient = recipient
        else:
            raise TypeError("Wrong Type")
        self.allMessage.append(self)

    def display(self):
        print(f"Time: {self.time}")
        print(f"Recipient: {self.recipient}")
        print(f"Sender: {self.sender}")
        print(f"Content: {self.content}")

    def reply(self, message_info):
        from app import line_bot_api
        from linebot.models import TextSendMessage
        import msg_templates
        send_msg = TextSendMessage(text="Your previous message:\n\""+self.content+"\"")
        line_bot_api.push_message(self.sender.line_userid, messages=send_msg)
        send_msg = msg_templates.get_sender_message(self.recipient.name, "Replied:\n\""+message_info+"\"")
        line_bot_api.push_message(self.sender.line_userid, messages=send_msg)

    @staticmethod
    def toJson(path=os.path.expanduser("~/ehealth/linebot/data/messages.json")): # 打包成Json，User的Obj是用line userid存
        with open(path, 'w') as file:
            l = []
            for msg in Message.allMessage:
                temp = vars(msg)
                temp["sender"] = temp["sender"].line_userid
                temp["recipient"] = temp["recipient"].line_userid
                l.append(temp)
            json.dump(l, file, indent=2)
    
    @staticmethod
    def loadJson(path=os.path.expanduser("~/ehealth/linebot/data/messages.json")): # 還原
        Message.allMessage.clear()
        with open(path, 'r') as file:
            data = json.load(file)
            for msg_data in data:
                Message(**msg_data)
        return Message.allMessage
    
    @staticmethod
    def deleteOldMessage(): # 刪除一個禮拜以前的訊息，會自動儲存
        one_week_ago = datetime.now() - timedelta(days=7)
        old_messages = [message for message in Message.allMessage if datetime.strptime(message['time'], "%Y-%m-%d %H:%M:%S") < one_week_ago]
        for message in old_messages:
            Message.allMessage.remove(message)
        Message.toJson()

class Reservation: 
    allReservation = {}
    def __init__(self, doctor, patient, note, number=None, time=None): # number 是號碼牌
        self.time = datetime.now().strftime("%Y-%m-%d") if time==None else time
        self.doctor = doctor
        self.note = note
        if type(patient) == type(str()):
            for user in User.allUsers:
                if user.line_userid == patient:
                    self.patient = user
        elif isinstance(patient, User):
            self.patient = patient
        else:
            raise TypeError("Wrong Type")
        if type(doctor) == type(str()):
            for user in User.allUsers:
                if user.line_userid == doctor:
                    self.doctor = user
        elif isinstance(doctor, User):
            self.doctor = doctor
        else:
            raise TypeError("Wrong Type")
        if number:
            self.number = number
        elif self.time not in Reservation.allReservation.keys():
            self.number = 0
            Reservation.allReservation[self.time] = []
        else:
            self.number = len(Reservation.allReservation[self.time])
        if self.time not in Reservation.allReservation.keys():
            Reservation.allReservation[self.time] = []
        Reservation.allReservation[self.time].append(self)

    @staticmethod
    def toJson(path=os.path.expanduser("~/ehealth/linebot/data/reservation.json")): # 打包成Json，User的Obj是用line userid存
        d = Reservation.allReservation.copy()
        with open(path, 'w') as file:
            for key in d.keys():
                d[key] = [vars(user) for user in d[key]]
                for j in range(len(d[key])):
                    d[key][j]["doctor"] = d[key][j]["doctor"].line_userid
                    d[key][j]["patient"] = d[key][j]["patient"].line_userid
            json.dump(d, file, indent=2)
    
    @staticmethod
    def loadJson(path=os.path.expanduser("~/ehealth/linebot/data/reservation.json")): # 同 Message
        Reservation.allReservation = {}
        with open(path, 'r') as file:
            data = json.load(file)
            for key in data.keys():
                for index in data[key]:
                    Reservation(**index)
        return Reservation.allReservation

if __name__ == "__main__":
    doctor = Doctor(name="TestDoctor", line_userid="dr.test.id", password="dr.test.pass")
    Doctor(name="Dohn Joe", line_userid="123", password="password")
    patient = Patient(name="TestPatient", birth_date="0916", id_number="T123", phone="test", line_userid="pt.test.id")
    Patient(name="Kappa", birth_date="1001", id_number="A131", phone="phone", line_userid="Ufc4c95ce42186b6965c5f684fa38c1a1")
    doctor.toJson()
    print(doctor.loadJson())
    doctor.toJson()

    Message("dr.test.id", "pt.test.id", "Hello World 1")
    Message("dr.test.id", "pt.test.id", "Test Hello 2")
    Message.toJson()
    Message.loadJson()
    Message.toJson()

    Reservation(doctor,patient,"Test info1")
    Reservation("dr.test.id","pt.test.id","Test info2")
    Reservation.toJson()
    print(Reservation.loadJson())
    Reservation.toJson()

    # User.loadJson()
    # Message.loadJson()
    # Reservation.loadJson()
    # Message.allMessage[2].reply("What is YOUR PROBLEM!!!")
