from commands.private.server_administrator import Admin
from commands.private.server_sql import ServerSQL

from commands.special.server_increase import server_increase
from commands.special.server_status import server_data
from commands.special.server_poke import server_poke
from commands.special.server_kunkun import KunKun_Game
from commands.special.server_schedule import Schedule

from commands.public.server_help import server_at, server_help
from commands.public.server_image import random_image, key_image
from commands.public.server_recall import server_recall
from commands.public.server_deepseek import DeepSeekServer


class Distribution(object):
    
    # 通过判断信息选择合适方法的函数
    def function_selection(self, message_dict: dict, event_type: str, manage_dict: dict) -> dict:
        
        if event_type == "message":
            return self.message_select(message_dict, manage_dict)
        
        if event_type == "notice":
            return self.notice_select(message_dict, manage_dict)

    def message_select(self, message_dict: dict, manage_dict: dict) -> dict:

        if message_dict["message_type"] == "private" or message_dict["user_id"] in manage_dict["private"]:
            message_send = self.private_message(message_dict)
            if message_send:
                return message_send
        
        if message_dict["message_type"] == "private" or message_dict["group_id"] in manage_dict["special"]:
            message_send = self.special_message(message_dict)
            if message_send:
                return message_send
            
        if message_dict:
            message_send = self.public_message(message_dict)
            if message_send:
                return message_send
            
        return None
    
    def notice_select(self, message_dict: dict, manage_dict: dict) -> dict:
        
        # if message_dict["user_id"] in manage_dict["private"]:
        #     pass
        
        if message_dict["group_id"] in manage_dict["special"]:
            message_send = self.special_notice(message_dict)
            if message_send:
                return message_send
            
        # if message_dict:
        #     pass
        
        return None

    def private_message(self, message_dict: dict) -> dict:
        
        for message_content in message_dict["message"]:
            if message_content["type"] == "text":
                
                # 高级帮助
                if message_content["data"]["text"] == "高级帮助":
                    return server_help(message_dict, "private_help")
                
                if len(message_content["data"]["text"]) < 12:
                    return None
                
                # (SQL_create/SQL_add/SQL_get/SQL_update/SQL_delete):(*.db):()
                if message_content["data"]["text"][:3] == "SQL":
                    return ServerSQL(message_dict, message_content["data"]["text"].split(":")).send()
                
                # (Admin) (group_add/group_delete/user_add/user_delete) (group_id)
                if message_content["data"]["text"][:5] == "Admin":
                    return Admin(message_dict, message_content["data"]["text"].split(" ")).send()
                
                # (SCHEDULE_add/SCHEDULE_delete/SCHEDULE_completed/SCHEDULE_check) (SCHEDULE)
                if message_content["data"]["text"][:8] == "SCHEDULE":
                    return Schedule(message_dict, message_content["data"]["text"].split(" "), "private_table").send()
                
        return None

    def special_message(self, message_dict: dict) -> dict:
        
        for message_content in message_dict["message"]:
            if message_content["type"] == "text":
                
                if message_content["data"]["text"] == "帮助":
                    return server_help(message_dict, "special_help")
                
                if message_content["data"]["text"].strip(" ") in ["创建牛至", "嗦牛至", "打胶", "透群友", "击剑"]:
                    return KunKun_Game().judge(message_dict, message_content["data"]["text"].strip(" "))
                
                if message_content["data"]["text"] == "服务器状态":
                    return server_data(message_dict, "服务器状态")
                
                if len(message_content["data"]["text"]) > 12 and message_content["data"]["text"][:8] == "schedule":
                    return Schedule(message_dict, message_content["data"]["text"].split(" "), "special_table").send()
                
        return None
    
    def public_message(self, message_dict: dict) -> dict:
        
        for message_content in message_dict["message"]:
            
            if message_content["type"] == "at":
                if message_content["data"]["qq"] == str(message_dict["self_id"]):
                    return server_at(message_dict)
            
            if message_content["type"] == "text":

                if message_content["data"]["text"][:2] == "ds":
                    return DeepSeekServer(message_dict, message_content["data"]["text"]).send()

                if len(message_content["data"]["text"]) < 4:
                    return None
                if len(message_content["data"]["text"]) > 12:
                    return None
                if message_content["data"]["text"] == "帮助":
                    return server_help(message_dict, "public_help")
                if message_content["data"]["text"][:2] == "p站":
                    return key_image(message_dict, message_content["data"]["text"])
                if message_content["data"]["text"] == "随机二次元":
                    return random_image(message_dict)
                if message_content["data"]["text"].strip(" ") == "消息撤回":
                    return server_recall(message_dict)
        
        return None
    
    def private_notice(self, message_dict: dict) -> dict:
        return None
    
    def special_notice(self, message_dict: dict) -> dict:
        
        if message_dict["notice_type"] == "group_increase":
            return server_increase(message_dict)
        if "sub_type" in message_dict and message_dict["sub_type"] == "poke":
            return server_poke(message_dict)
        
        return None
    
    def public_notice(self, message_dict: dict) -> dict:
        return None