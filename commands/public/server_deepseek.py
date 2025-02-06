
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from commands.method.deepseek import DeepSeekAPI

deepseek = DeepSeekAPI()

class DeepSeekServer(object):

    def __init__(self, message_dict: dict, message_list: str):
        self.message_dict = message_dict
        self.command = message_list[0]
        self.group_text = ""
        for i in range(1, len(message_list)):
            self.group_text += message_list[i] + " "
        self.group_text = self.group_text[:-1]
        
    def send(self):
        
        user_list = Parameter_Judgment().parameter_judgment(self.message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        message_text = "正在思考喵~"
        
        if self.command == "ds-":
            message_text = DeepSeekAPI.start_new_conversation()
        elif self.command == "ds0":
            message_text = deepseek.async_chat(self.group_text, 0.0, message)
        elif self.command == "ds1":
            message_text = deepseek.async_chat(self.group_text, 1.0, message)
        elif self.command == "ds2":
            message_text = deepseek.async_chat(self.group_text, 1.3, message)
        elif self.command == "ds3":
            message_text = deepseek.async_chat(self.group_text, 1.5, message)
        else:
            message_text = "主人，喵~\n输入的指令有误，喵~"
            
        return message.at_message(self.message_dict["user_id"], message_text)
    