from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from config import settings

def server_poke(message_dict):

    settings.PokeConfig.POKE_COUNT += 1
    if settings.PokeConfig.POKE_COUNT >= 3:
        settings.PokeConfig.POKE_COUNT = 0
        user_list = Parameter_Judgment().parameter_judgment(message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        return message.normal_message("别戳了，再戳就坏了喵！~~>_<~~")
    else:
        return None
 