
from function.message_sendformat import Message_SendFormat, Parameter_Judgment
from function.database import OnebotDatabase
import sqlite3

class Admin(object):

    def __init__(self, message_dict: dict, message_list: str):
        self.message_dict = message_dict
        self.command = message_list[1]
        self.admin_text = message_list[2]
        
    def send(self):
        
        con, cur, admin_object = self.admin_database("database")
        
        if self.command == "group_add":
            message_text = self.group_add(con, cur)
        elif self.command == "group_delete":
            message_text = self.group_delete(con, cur)
        elif self.command == "user_add":
            message_text = self.user_add(con, cur)
        elif self.command == "user_delete":
            message_text = self.user_delete(con, cur)
        else:
            message_text = "主人，喵~\n输入的指令有误，喵~"
    
        user_list = Parameter_Judgment().parameter_judgment(self.message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        admin_object.close(con, cur)
        return message.at_message(self.message_dict["user_id"], message_text)
        
    # 读取计划数据库
    def admin_database(self, path: str) -> tuple[list[int], sqlite3.Connection, sqlite3.Cursor, OnebotDatabase]:
        admin = OnebotDatabase(path)
        con, cur = admin("special_manage.db")
        return con, cur, admin
    
    def group_add(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        cur.execute("SELECT * FROM special WHERE group_id=?", (self.admin_text,))
        if cur.fetchone():
            return "主人，喵~\n这个群已经在库中了，喵~"
        
        cur.execute("INSERT INTO special (group_id) VALUES (?)", (self.admin_text,))
        con.commit()
        return "主人，喵~\n这个群已经加入库了，喵~"
    
    def group_delete(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        cur.execute("SELECT * FROM special WHERE group_id=?", (self.admin_text,))
        if not cur.fetchone():
            return "主人，喵~\n这个群不在库中，喵~"
        
        cur.execute("DELETE FROM special WHERE group_id=?", (self.admin_text,))
        con.commit()
        return "主人，喵~\n这个群已经删除了，喵~"
    
    def user_add(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        cur.execute("SELECT * FROM private WHERE user_id=?", (self.admin_text,))
        if cur.fetchone():
            return "主人，喵~\n这个用户已经在库中了，喵~"
        
        cur.execute("INSERT INTO private (user_id) VALUES (?)", (self.admin_text,))
        con.commit()
        return "主人，喵~\n这个用户已经加入库了，喵~"
    
    def user_delete(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        
        cur.execute("SELECT * FROM private WHERE user_id=?", (self.admin_text,))
        if not cur.fetchone():
            return "主人，喵~\n这个用户不在库中，喵~"
        
        cur.execute("DELETE FROM private WHERE user_id=?", (self.admin_text,))
        con.commit()
        return "主人，喵~\n这个用户已经删除了，喵~"
    