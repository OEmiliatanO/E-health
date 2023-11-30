from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
from user import *
import datetime

def info_check(userId):
    for user in User.allUsers:
        if user.line_userid == userId:
            return user
    else:
        return False
