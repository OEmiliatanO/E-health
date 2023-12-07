import json
from datetime import datetime, timedelta
import user as fish

#it will be modify later to correct path
from API import * 
from pinfo import med_record_t, patient_info_t

def get_patients_info_by_id(s12782514: str, path="../DB/central_DB")-> patient_info_t:
    api = DB_API()
    api.set_DB(DB_factory.create(DB_factory.plain_text_DB), path)
    info = api.load_info(s12782514)
    return info

def create_patients_info_by_id(s12782514: str, pinfo: pinfo.patient_info_t, path="../DB/central_DB") -> None: # 謝承翰的UID為身分證字號(id_number)
    api = DB_API()
    api.set_DB(DB_factory.create(DB_factory.plain_text_DB), path)
    api.write_back(s12782514, pinfo)

def delete_chat(message_to_delete):
    for message in fish.Message.allMessage:
        if message == message_to_delete:
            fish.Message.allMessage.remove(message)
            return

def pack_chat(Matched_chat, page_pack=3):
    packed_chat = [Matched_chat[i:i + page_pack] for i in range(0, len(Matched_chat), page_pack)]
    return packed_chat

def browse_chat(doctor_name, pack=True, page_pack=3):
    Matched_chat = []
    for message in fish.Message.allMessage:
        recipient_name = message.recipient.name
        if recipient_name == doctor_name:
            Matched_chat.append(message)
    if(pack):
        Matched_chat = pack_chat( Matched_chat, page_pack)
    return Matched_chat

def Doctor_login(name, password):
    for user in fish.User.allUsers:
        # print("fuck",user.line_userid)
        if(user.name == name):
            if(user.permission!="doctor"):
                print("permission 錯誤")
                return False
            if(user.password == password):
                print("Link start")
                return True
            else:
                print("密碼錯誤")
                return False
    else:
        print("找不到此名字")
        return False

def delete_reservation(item_to_delete):
    for date, reservation_list in fish.Reservation.allReservation.items():
        for reservation_item in reservation_list:
            # Assuming item_to_delete is a unique identifier for the item to be deleted
            if reservation_item == item_to_delete:
                reservation_list.remove(reservation_item)
                print(f"Item {item_to_delete} deleted successfully.")
                return

def edit_reservation(item_to_edit, time=None, number=None, note=None):
    for date, reservation_list in fish.Reservation.allReservation.items():
        for reservation_item in reservation_list:
            # Assuming item_to_edit is a unique identifier for the item to be edited
            if reservation_item == item_to_edit:
                if time is not None:
                    reservation_item.time = time
                if number is not None:
                    reservation_item.number = number
                if note is not None:
                    reservation_item.note = note

                print(f"Item {item_to_edit} edited successfully.")
                return
    print(f"Item {item_to_edit} not found in reservations.")

def pack_reservation(Matched_resv, page_pack = 3):
    Matched_resv = [Matched_resv[i:i + page_pack] for i in range(0, len(Matched_resv), page_pack)]
    return Matched_resv

def browse_reservation(doctor_name, pack=True, page_pack=3):
    Matched_resv = []
    for resv_id, resv_list in fish.Reservation.allReservation.items():
        for resv in resv_list:
            if resv.doctor.name == doctor_name:
                Matched_resv.append(resv)
    if pack:
        Matched_resv = pack_reservation(Matched_resv, page_pack)
    return Matched_resv

def json_initiallized():
    fish.User.loadJson() #load json file
    fish.Message.loadJson()
    fish.Reservation.loadJson()


def add_test():
    fish.Reservation("123","0091","fucking Bitch")
    fish.Reservation("123","0091","damn fucking Bitch")
    fish.Message("123", "0091", "You are a doctor?\n what subject you studied?")
    fish.Message("123", "0091", "sir i got cancer jal;fjkasdjfkdsjaflajfkasfja;ajk")
    fish.Message("123", "0091", "sir i run out of money")
    fish.Message("123", "0091", "sir i have a crush on you")
    fish.Message("123", "0091", "Sir I really have a feeling on you\n I just wanna tell you how I'm feeling\nGotta make you understand\nNever gonna give you up\nNever gonna let you down\nNever gonna run around and desert you\nNever gonna make you cry\nNever gonna say goodbye\nNever gonna tell a lie and hurt you")
    
if __name__ == "__main__":
    fish.User.loadJson() #load json file
    fish.Message.loadJson()
    fish.Reservation.loadJson()

    print(browse_reservation("John Doe"))
    
    c = fish.Message("123", "0091", "sir i got cancer")
    print(c.recipient)
    print(fish.Message.allMessage)
    print(browse_chat("John Doe"))

    print(get_patients_info_by_id("0001"))