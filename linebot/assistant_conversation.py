import random

def hello_conv(user_name):
    hello_conv1 = [
        "Good Moring, ",
        "Hello, ",
        "Would you like a cup of joe? ",
        "You are late, ",
        "You are so early, ",
        "Yo, ",
        "Yahalo, ",][random.randint(0, 6)]
    
    hello_conv2 = [
        user_name, 
        "Doctor", 
        "MY LOVE",
        "bro"][random.randint(0, 3)] + "."
    return hello_conv1 + hello_conv2

def daily_conversation_to_doctor(user_name):
    daily_conv1 = [
        "How was your morning, Dr. ",
        "Do you have a moment to discuss today's schedule, Dr. ",
        "Any updates on the patient reports, Dr. ",
        "Is there anything specific you'd like to address today, Dr. ",
        "Have you reviewed the recent test results, Dr. ",
        "Is there anything I can assist you with today, Dr. ",
        "Do you have any meetings scheduled for today, Dr. ",]

    daily_conv2 = user_name + "?"

    return random.choice(daily_conv1) + daily_conv2