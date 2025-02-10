
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from commands.method.deepseek import DeepSeekAPI
from config import settings
import json

with open(settings.PathConfig.CONFIG_JSON) as f:
    temp = json.load(f)
    settings.DeepSeekConfig.API_KEY = temp['deepseek']['key']
    settings.DeepSeekConfig.API_URL = temp['deepseek']['url']

deepseek = DeepSeekAPI()

class DeepSeekServer(object):

    def __init__(self, message_dict: dict, message_str: str):
        self.message_dict = message_dict
        self.command = message_str[:3]
        self.group_text = message_str[3:]
        
    def send(self):
        
        user_list = Parameter_Judgment().parameter_judgment(self.message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        message_text = "正在思考喵~"
        if self.group_text == " ":
            message_text = "主人，请输入对话内容喵~"
        elif self.command == "ds-":
            DeepSeekAPI.start_new_conversation()
            message_text = "已经开始新的对话喵~"
        elif self.command == "ds0":
            deepseek.async_chat(self.group_text, 0.0, message)
        elif self.command == "ds1":
            deepseek.async_chat(self.group_text, 1.0, message)
        elif self.command == "ds2":
            deepseek.async_chat(self.group_text, 1.3, message)
        elif self.command == "ds3":
            deepseek.async_chat(self.group_text, 1.5, message)
        elif self.command == "ds4":
            deepseek.async_chat(self.group_text, 2, message)
        else:
            message_text = "主人，输入的指令有误喵~"
            
        return message.at_message(self.message_dict["user_id"], message_text)
    