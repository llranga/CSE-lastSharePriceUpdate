import requests

class TelegramMessage:
    def __init__(self,bot_token:str,chat_id:str):
        self.bot_token=bot_token
        self.chat_id=chat_id
        

    def send_message(self,message):
        '''send message in string'''
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        data = {
            "chat_id": self.chat_id,
            "text": message
        }
        requests.post(url, data=data)
        #print("Message sent")