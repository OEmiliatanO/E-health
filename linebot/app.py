from flask import Flask, request, abort, render_template
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from utils import *
import msg_templates
import os
import base64

CHANNEL_SECRET = "904aca20c4045a8d34bb285cb96ead79"
CHANNEL_ACCESS_TOKEN = "P4kyLQq9aSYYlMtpLEsSM4oD2bG3oMk8RfL29Baf2BUWLLRQMf/4QdKKam46fVQXpZeL3By9GzS8VZgjB0LTdvSTIOt8foBIt5cn0nyFgwkoZNq4r7bsewFuw0OIINgenaeQ/FvJYwd2XLZ+lzRq9wdB04t89/1O/w1cDnyilFU="
WEBSITE = "https://867f-61-227-117-60.ngrok-free.app"

app = Flask(__name__, template_folder="templates")

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

d = {}

@app.route('/message/<line_userid>', methods=['GET', 'POST'])
def message_request(line_userid):
    items = ['Option 1', 'Option 2', 'Option 3']

    if request.method == 'POST':
        selected_option = request.form.get('options')
        encoded_content = request.form.get('encoded_content')
        print(line_userid, selected_option, encoded_content, sep='\n')

        return render_template('messages_confirmation.html')

    return render_template('messages.html', line_userid=line_userid, items=items)



@app.route('/register/<line_userid>', methods=['GET', 'POST'])
def index(line_userid):
    if request.method == 'POST':
        # 從表單中獲取使用者輸入的資訊
        name = request.form['name']
        birth_date = request.form['birth_date']
        id_number = request.form['id_number']
        phone = request.form['phone']
        blood_type = request.form.get('blood_type')
        emergency_contact = request.form.get('emergency_contact')
        emergency_contact_phone = request.form.get('emergency_contact_phone')
        email = request.form.get('email')
        height = request.form.get('height')
        weight = request.form.get('weight')
        medical_history = request.form.get('medical_history')
        notes = request.form.get('notes')
        d[line_userid] = name
        return render_template("register_confirmation.html", name=name)
    return render_template("register.html", line_userid=line_userid)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    userId = event.source.user_id
    msg = event.message.text
    if msg == "!reg":
        button = msg_templates.get_register_button(WEBSITE, userId)
        line_bot_api.reply_message(event.reply_token, button)
    elif msg=='!reserve':
        send_msg = msg_templates.get_send_reserve_message(userId)
        line_bot_api.reply_message(event.reply_token, send_msg)
    elif msg=="!talk":
        send_msg = msg_templates.get_sender_message("Dr. Lin", "You got cancer.")
        line_bot_api.reply_message(event.reply_token, send_msg)
    elif userId in d.keys():
        send_msg = TextSendMessage(text=f"Your name is {d[userId]}")
        line_bot_api.reply_message(event.reply_token, send_msg)
    else:
        send_msg = TextSendMessage(text=f"Your user id is {userId}")
        line_bot_api.reply_message(event.reply_token, send_msg)

@handler.add(PostbackEvent)
def handle_postback(event):
    userId = event.source.user_id
    if event.postback.data == 'action=selectDateTime':
        reserved_date = event.postback.params['date']
        reserve_data(reserved_date,userId)
        send_msg = TextSendMessage(text=f"Your reservation is succeed: {reserved_date}")
        line_bot_api.reply_message(event.reply_token, send_msg)

if __name__ == "__main__":
    app.run()
