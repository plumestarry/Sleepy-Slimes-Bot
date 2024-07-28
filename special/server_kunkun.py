
from function.message_sendformat import Message_SendFormat, Parameter_Judgment
from function.database import OnebotDatabase
import random
import sqlite3

class KunKun_Game(object):
    
    def judge(self, message_dict: dict, message_text: str) -> dict:
        
        if message_dict["message_type"] != "group":
            return None
            
        user_list = Parameter_Judgment().parameter_judgment(message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])

        user_id_list, con, cur, member_object = self.member_database("database")
        
        if "创建牛至" in message_text:
            return self.func1(message_dict, message, user_id_list, con, cur, member_object)
        
        elif message_dict["user_id"] not in user_id_list:
            return self.func0(message_dict, message)
        
        elif "嗦牛至" in message_text:
            return self.func2(message_dict, message, con, cur, member_object)
        
        elif "打胶" in message_text:
            return self.func3(message_dict, message, con, cur, member_object)
        
        elif "透群友" in message_text:
            return self.func4(message_dict, message, user_id_list, con, cur, member_object)
        
        elif "击剑" in message_text:
            return self.func5(message_dict, message, user_id_list, con, cur, member_object)
        
        else:
            return None
    
    # 读取成员数据库
    def member_database(self, path: str) -> tuple[list[int], sqlite3.Connection, sqlite3.Cursor, OnebotDatabase]:
        member = OnebotDatabase(path)
        con, cur = member("kunkun_data.db")
        member_id_list = []
        for member_id in member.get_data(con, cur, "user_id", "kunkun"):
            member_id_list.append(member_id[0])
        return member_id_list, con, cur, member
    
    # 若没有牛至则返回
    def func0(self, message_dict: dict, message: Message_SendFormat) -> dict:
        
        return message.at_message(message_dict["user_id"], "主人您还没有创建牛至喵~，是否先创建牛至喵~，输入“创建牛至”即可创建喵~，创建了牛至可以实现以下功能喵~\n\n1. 嗦牛至\n2. 打胶\n3. @群友 透群友\n4. @群友 击剑")
    
    # 创建牛至
    def func1(self, message_dict: dict, message: Message_SendFormat, user_id_list: list[int], con: sqlite3.Connection, cur: sqlite3.Cursor, member_object: OnebotDatabase) -> dict:
        
        if message_dict["user_id"] in user_id_list:
            length = cur.execute("SELECT 长度 FROM kunkun WHERE user_id={}".format(message_dict["user_id"])).fetchone()[0]
            member_object.close(con, cur)
            if length < 0:
                return message.at_message(message_dict["user_id"], "主人您只有小学了喵~ 无法再创建牛至了喵~")
            return message.at_message(message_dict["user_id"], "主人您已经有牛至了喵~")

        else:
            cur.execute("INSERT INTO {} (user_id, 长度, 倍率, 嗦牛至, 打胶, 透群友, 被透, 击剑) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                        .format("kunkun"), 
                        (message_dict['user_id'], 10.00, 1.00, 0, 0, 0, 0, 0))
            con.commit()
            member_object.close(con, cur)
            return message.at_message(message_dict["user_id"], "主人已经为您创建牛至了喵~，初始长度为10.00cm喵~")

    # 嗦牛至
    def func2(self, message_dict: dict, message: Message_SendFormat, con: sqlite3.Connection, cur: sqlite3.Cursor, member_object: OnebotDatabase) -> dict:
            
        user_tuple = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(message_dict["user_id"])).fetchone()
        
        if user_tuple[2] < 0:
            return message.at_message(message_dict["user_id"], "主人您已经没有牛至了喵~，无法再嗦牛至了喵~")
            
        random_length = random.uniform(1.0, 2.5)
        if 1.13 < random_length < 1.15:
            random_length = 11.45
        
        random_length = round(random_length, 2)
        update_length = round(user_tuple[2] + random_length, 2)
        cur.execute("UPDATE kunkun SET 长度=? WHERE user_id=?", (update_length, message_dict["user_id"]))
        cur.execute("UPDATE kunkun SET 嗦牛至=? WHERE user_id=?", (user_tuple[4] + 1, message_dict["user_id"]))
        con.commit()
        member_object.close(con, cur)
        
        return message.at_message(message_dict["user_id"], "主人您的牛至长度增加了{}cm喵~，长度变化为{}cm喵~".format(random_length, update_length))
    
    # 打胶
    def func3(self, message_dict: dict, message: Message_SendFormat, con: sqlite3.Connection, cur: sqlite3.Cursor, member_object: OnebotDatabase) -> dict:
        
        user_tuple = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(message_dict["user_id"])).fetchone()
        
        if user_tuple[2] < 0:
            return message.at_message(message_dict["user_id"], "主人您已经没有牛至了喵~，无法再打胶了喵~")
            
        random_multiplier = round(random.uniform(0, 0.2), 2)
        update_length = round(user_tuple[3] + random_multiplier, 2)
        cur.execute("UPDATE kunkun SET 倍率=? WHERE user_id=?", (update_length, message_dict["user_id"]))
        cur.execute("UPDATE kunkun SET 打胶=? WHERE user_id=?", (user_tuple[5] + 1, message_dict["user_id"]))
        con.commit()
        member_object.close(con, cur)
        
        return message.at_message(message_dict["user_id"], "主人您的持久率增加了{}喵~，当前持久率提升为{}，可以透更多了喵~".format(random_multiplier, update_length))
    
    # 透群友
    def func4(self, message_dict: dict, message: Message_SendFormat, user_id_list: list[int], con: sqlite3.Connection, cur: sqlite3.Cursor, member_object: OnebotDatabase) -> dict:

        user_tuple_1 = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(message_dict["user_id"])).fetchone()
        if user_tuple_1[2] < 0:
            return message.at_message(message_dict["user_id"], "主人您已经没有牛至了喵~，只能被透了喵~")

        user_id_2 = 1044113073
        random_time = round(random.uniform(10, 25), 1)
        random_ml = round(5 * user_tuple_1[3], 2)
        if 11.3 < random_time < 11.5:
            random_time = 114
            random_ml = 514
        cur.execute("UPDATE kunkun SET 透群友=? WHERE user_id=?", (user_tuple_1[6] + 1, message_dict["user_id"]))
        con.commit()
        
        # 若未指定用户则随机选择
        if len(message_dict["message"]) == 1:
            all_user_list = []
            
            for all_user_id in cur.execute("SELECT user_id FROM group_user").fetchall():
                all_user_list.append(all_user_id[0])
            user_id_2 = all_user_list[random.randrange(0, len(all_user_list))]
            member_object.close(con, cur)
            try:        
                if user_id_2 not in all_user_list:
                    return message.at_message(message_dict["user_id"], "请试试其他人喵~")
                if user_id_2 not in user_id_list:
                    return message.at_at_message(message_dict["user_id"], f"花费了{random_time}秒向", user_id_2, f"注入了{random_ml}ml脱氧核糖核酸")
            except Exception as e:
                return None
            
        # 若指定用户则透指定用户
        for list_element in message_dict["message"]:
            if list_element["type"] == "at":
                user_id_2 = list_element["data"]["qq"]
        user_tuple_2 = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(user_id_2)).fetchone()
        cur.execute("UPDATE kunkun SET 被透=? WHERE user_id=?", (user_tuple_2[7] + 1, user_id_2))
        
        if user_tuple_2[2] < -60:
            member_object.close(con, cur)
            return message.at_message(user_id_2, "的小学已经透到极限了，不能再透了哦~")
        
        if user_tuple_2[2] < 0:
            
            length = abs((user_tuple_2[2] - user_tuple_1[2]) / 20)
            length_1 = abs(round(random.uniform(length * -1.5, length), 2))
            length_2 = -length_1
        
            cur.execute("UPDATE kunkun SET 长度=? WHERE user_id=?", (round(user_tuple_1[2] + length_1, 2), message_dict["user_id"]))
            cur.execute("UPDATE kunkun SET 长度=? WHERE user_id=?", (round(user_tuple_2[2] + length_2, 2), user_id_2))
        
        con.commit()
        member_object.close(con, cur)
        if user_tuple_2[2] + length_2 < 0:
            dict_text_2_length = round(user_tuple_2[2] + length_2, 2)
            return message.at_at_message(message_dict["user_id"], f"花费了{random_time}秒向", user_id_2, f"注入了{random_ml}ml脱氧核糖核酸，使其小学拓展了{length_1}cm，变化为{dict_text_2_length}cm")

        return message.at_at_message(message_dict["user_id"], f"花费了{random_time}秒向", user_id_2, f"注入了{random_ml}ml脱氧核糖核酸")
    
    # 击剑
    def func5(self, message_dict: dict, message: Message_SendFormat, user_id_list: list[int], con: sqlite3.Connection, cur: sqlite3.Cursor, member_object: OnebotDatabase) -> dict:

        # 获取击剑对象
        for list_element in message_dict["message"]:
            if list_element["type"] == "at":
                user_id_2 = list_element["data"]["qq"]
        try:        
            if user_id_2 not in user_id_list:
                return message.at_message(message_dict["user_id"], "对方还未创建牛至喵~")
        except Exception as e:
            pass
        
        if len(message_dict["message"]) == 1:
            user_id_2 = user_id_list[random.randrange(0, len(user_id_list))]
        
        
        user_tuple_1 = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(message_dict["user_id"])).fetchone()
        user_tuple_2 = cur.execute("SELECT * FROM kunkun WHERE user_id={}".format(user_id_2)).fetchone()
        if user_tuple_1[2] < 0:
            return message.at_message(message_dict["user_id"], "主人您已经没有牛至了喵~，只能被对方透了喵~")
        if user_tuple_2[2] < 0:
            return message.at_message(message_dict["user_id"], "主人，对方已经没有牛至了喵~，只能透对方了喵~")
        
        length = abs((user_tuple_2[2] - user_tuple_1[2]) / 20)
        length_1 = round(random.uniform(length * -1.5, length), 2)
        length_2 = -length_1
        
        cur.execute("UPDATE kunkun SET 击剑=? WHERE user_id=?", (user_tuple_1[8] + 1, message_dict["user_id"]))
        cur.execute("UPDATE kunkun SET 击剑=? WHERE user_id=?", (user_tuple_2[8] + 1, user_id_2))
        cur.execute("UPDATE kunkun SET 长度=? WHERE user_id=?", (round(user_tuple_1[2] + length_1, 2), message_dict["user_id"]))
        cur.execute("UPDATE kunkun SET 长度=? WHERE user_id=?", (round(user_tuple_2[2] + length_2, 2), user_id_2))
        con.commit()
        member_object.close(con, cur)
        
        str_1 = "的牛至增长了{}cm，目前长度为{}cm。".format(length_1, round(user_tuple_1[2] + length_1, 2))
        if length_1 < 0:
            str_1 = "的牛至缩短了{}cm，目前长度为{}cm。".format(-length_1, round(user_tuple_1[2] + length_1, 2))
        str_2 = "的牛至增长了{}cm，目前长度为{}cm。".format(length_2, round(user_tuple_2[2] + length_2, 2))
        if length_2 < 0:
            str_2 = "的牛至缩短了{}cm，目前长度为{}cm。".format(-length_2, round(user_tuple_2[2] + length_2, 2))
        
        return message.at_at_message(message_dict["user_id"], str_1, user_id_2, str_2)
        
