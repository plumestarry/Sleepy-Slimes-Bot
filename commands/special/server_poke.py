from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from config import settings

def server_poke(message_dict):

    message = Message_SendFormat("send_group_msg", "group_id", message_dict["group_id"])
    settings.PokeConfig.POKE_COUNT += 1
    if settings.PokeConfig.POKE_COUNT >= 3:
        settings.PokeConfig.POKE_COUNT = 0
        return message.normal_message("别戳了，再戳就坏了喵！~~>_<~~")
    else:
        return message.normal_message("~>_<~")
 