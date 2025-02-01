from function.message_sendformat import Message_SendFormat, Parameter_Judgment
from function.database import OnebotDatabase
import sqlite3

class Schedule(object):
    
    def __init__(self, message_dict: dict, message_list: str, table_name: str):
        self.message_dict = message_dict
        self.command = message_list[0].split("_")[1]
        self.schedule_text = message_list[1]
        self.table_name = table_name
        
    def send(self):
        
        con, cur, schedule_object = self.schedule_database("database")
        
        if self.command == "add":
            message_text = self.schedule_add(con, cur)
        elif self.command == "delete":
            message_text = self.schedule_delete(con, cur)
        elif self.command == "completed":
            message_text = self.schedule_completed(con, cur)
        elif self.command == "check":
            message_text = self.schedule_check(con, cur)
        else:
            message_text = "主人，喵~\n输入的指令有误，喵~"
    
        user_list = Parameter_Judgment().parameter_judgment(self.message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        schedule_object.close(con, cur)
        return message.at_message(self.message_dict["user_id"], message_text)
        
    # 读取计划数据库
    def schedule_database(self, path: str) -> tuple[list[int], sqlite3.Connection, sqlite3.Cursor, OnebotDatabase]:
        schedule = OnebotDatabase(path)
        con, cur = schedule("schedule.db")
        return con, cur, schedule
    
    # 添加计划
    def schedule_add(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        print("qww")
        cur.execute("INSERT INTO {} (添加者, 添加时间, 完成者, 完成时间, 删除者, 删除时间, 当前状态, 计划内容) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                    .format(self.table_name), 
                    (self.message_dict['user_id'], self.message_dict['time'], 0, 0, 0, 0, 0, self.schedule_text))
        con.commit()
        schedule_id = cur.execute("SELECT id FROM {} WHERE 添加时间={}".format(self.table_name, self.message_dict["time"])).fetchone()[0]
        return "计划添加成功喵~，您添加的计划id为{}，喵~".format(schedule_id)
    
    def schedule_completed(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        state = cur.execute("SELECT 当前状态 FROM {} WHERE id={}".format(self.table_name, int(self.schedule_text))).fetchone()
        if not state:
            return "计划不存在喵~"
        if state[0] == 1:
            return "计划早已经了完成喵~不能再完成一次了喵~"
        if state[0] == 2:
            return "计划已删除了喵~不能再完成了喵~"
        
        cur.execute("UPDATE {} SET 完成者=?, 完成时间=?, 当前状态=? WHERE id=?".format(self.table_name), (self.message_dict["user_id"], self.message_dict["time"], 1, int(self.schedule_text)))
        con.commit()
        return "计划完成了喵~真是太棒了喵~"
    
    def schedule_delete(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        state = cur.execute("SELECT 当前状态 FROM {} WHERE id={}".format(self.table_name, int(self.schedule_text))).fetchone()
        if not state:
            return "计划不存在喵~"
        if state[0] == 1:
            return "计划已经了完成喵~不能删除喵~"
        if state[0] == 2:
            return "计划早已经删除了喵~不能再删除喵~"
        
        cur.execute("UPDATE {} SET 删除者=?, 删除时间=?, 当前状态=? WHERE id=?".format(self.table_name), (self.message_dict["user_id"], self.message_dict["time"], 2, int(self.schedule_text)))
        con.commit()
        return "计划已经删除了喵~"
    
    def schedule_check(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        schedule_string = ""
        
        if self.schedule_text == "未完成":
            schedule_string += "未完成的计划有：\n"
            if not cur.execute("SELECT id FROM {} WHERE 当前状态=0".format(self.table_name)).fetchone():
                return "没有未完成的计划喵~"
            for content in cur.execute("SELECT id, 计划内容 FROM {} WHERE 当前状态=0".format(self.table_name)).fetchall():
                schedule_string += f"{content[0]}. {content[1]}\n"
            return schedule_string
        
        if self.schedule_text == "已完成":
            schedule_string += "已完成的计划有：\n"
            if not cur.execute("SELECT id FROM {} WHERE 当前状态=1".format(self.table_name)).fetchone():
                return "没有已完成的计划喵~"
            for content in cur.execute("SELECT id, 计划内容 FROM {} WHERE 当前状态=1".format(self.table_name)).fetchall():
                schedule_string += f"{content[0]}. {content[1]}\n"
            return schedule_string
        
        if self.schedule_text == "已删除":
            schedule_string += "已删除的计划有：\n"
            if not cur.execute("SELECT id FROM {} WHERE 当前状态=2".format(self.table_name)).fetchone():
                return "没有已删除的计划喵~"
            for content in cur.execute("SELECT id, 计划内容 FROM {} WHERE 当前状态=2".format(self.table_name)).fetchall():
                schedule_string += f"{content[0]}. {content[1]}\n"
            return schedule_string
        
        return schedule_string

    
    