from commands.method.message_sendformat import Message_SendFormat
from commands.method.database import OnebotDatabase

def server_increase(message_dict) -> dict:
    
    message_text = ""
    database = OnebotDatabase("database/data")
    con, cur = database("special_manage.db")
    message_text = cur.execute("SELECT introduct FROM special WHERE group_id=?", (message_dict["group_id"],)).fetchone()[0]
    database.close(con, cur)
    message = Message_SendFormat("send_group_msg", "group_id", message_dict["group_id"])
    return message.at_message(message_dict["user_id"], message_text)

