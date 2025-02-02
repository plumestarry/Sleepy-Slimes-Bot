from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from config import settings
import json

def server_at(message_dict):

    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.at_message(message_dict["user_id"], "主人，喵~\n想知道如何使用我可以输入“帮助”，喵~")
        
def server_help(message_dict, help_path):
    
    message_text = ""
    with open(settings.PathConfig.HELP_JSON) as f:
        message_text = json.load(f)[help_path]
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.at_message(message_dict["user_id"], message_text)
