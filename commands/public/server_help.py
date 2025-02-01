from function.message_sendformat import Message_SendFormat, Parameter_Judgment

def server_at(message_dict):

    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.at_message(message_dict["user_id"], "主人，喵~\n想知道如何使用我可以输入“帮助”，喵~")
        
def server_help(message_dict, help_path):
    
    message_text = ""
    with open("database/{}.txt".format(help_path), "r", encoding="utf-8") as file:
        message_text = file.read()
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.at_message(message_dict["user_id"], message_text)
