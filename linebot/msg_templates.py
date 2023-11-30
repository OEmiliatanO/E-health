from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from linebot.models import Sender
import datetime

def get_register_button(website,line_userid):
    uri_button = URIAction(
        label='Open Website',
        uri=website+'/register/'+line_userid
    )
    # 建立 Buttons Template 訊息
    buttons_template = ButtonsTemplate(
        title='Register',
        text='Click the button to open the register website.',
        actions=[uri_button]
    )
    template_message = TemplateSendMessage(
        alt_text='Buttons Template',
        template=buttons_template
    )
    return template_message

def get_send_reserve_message(user_id):
    return FlexSendMessage(
                alt_text='Please choose your appointment time',
                contents={
                    'type': 'bubble',
                    'hero': {'type': 'image', 'url': 'https://i.imgur.com/nTQMxbg.jpg', 'size': 'full', 'aspectRatio': '20:13', 'aspectMode': 'cover'},
                    'body': {
                        'type': 'box',
                        'layout': 'vertical',
                        'contents': [
                            {'type': 'text', 'text': 'Reserve Date', 'weight': 'bold', 'size': 'xl'},
                            {'type': 'text', 'text': 'Choose Your Appointment Time', 'size': 'md', 'margin': 'md'},
                            {'type': 'button', 'action': {'type': 'datetimepicker','data': f'action=selectDateTime&user_id={user_id}', 'label': 'Choose Date', 'data': 'action=selectDateTime', 'mode': 'date', 'min':(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),'max': (datetime.datetime.now() + datetime.timedelta(days=7)).strftime('%Y-%m-%d')}},
                            {'type': 'button', 'action': {'type': 'uri', 'label': 'Contact Us', 'uri': 'tel:+886987331763'}}
                        ]
                    }
                }
            )

def get_sender_message(senderName, text):
    return TextSendMessage(
            text=text,
            sender=Sender(
                name=senderName,
                icon_url="https://i.imgur.com/xhw2cc2.png")
        )
