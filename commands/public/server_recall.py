from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment

def server_recall(message_dict) -> dict:
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    
    for message_content in message_dict["message"]:
        if message_content["type"] == "reply":
            message = Message_SendFormat("delete_msg", user_list[1], user_list[2])
            return message.recall_message(message_content["data"]["id"])
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.at_message(message_dict["user_id"], "未找到回复的消息")
