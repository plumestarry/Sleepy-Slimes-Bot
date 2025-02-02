from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from commands.method.database import OnebotDatabase
import sqlite3

class ServerSQL(object):

    def __init__(self, message_dict: dict, message_list: str):
        self.message_dict = message_dict
        self.command = message_list[0]
        self.sql_file = message_list[1]
        self.sql_text = ""
        for i in range(2, len(message_list)):
            self.sql_text += message_list[i] + ":"
        self.sql_text = self.sql_text[:-1]
        
    def send(self):
        
        con, cur, sql_object = self.sql_database("database/data")
        
        if self.command == "SQL_create":
            message_text = self.sql_command(con, cur)
        elif self.command == "SQL_add":
            message_text = self.sql_command(con, cur)
        elif self.command == "SQL_get":
            message_text = self.sql_get(con, cur)
        elif self.command == "SQL_update":
            message_text = self.sql_command(con, cur)
        elif self.command == "SQL_delete":
            message_text = self.sql_command(con, cur)
        else:
            message_text = "主人，喵~\n输入的指令有误，喵~"
    
        user_list = Parameter_Judgment().parameter_judgment(self.message_dict)
        message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
        sql_object.close(con, cur)
        return message.at_message(self.message_dict["user_id"], message_text)
        
    # 读取计划数据库
    def sql_database(self, path: str) -> tuple[list[int], sqlite3.Connection, sqlite3.Cursor, OnebotDatabase]:
        sql = OnebotDatabase(path)
        con, cur = sql("{}.db".format(self.sql_file))
        return con, cur, sql
    
    def sql_command(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        cur.execute(self.sql_text)
        con.commit()
        return "数据库操作成功，喵~"

    def sql_get(self, con: sqlite3.Connection, cur: sqlite3.Cursor) -> str:
        cur.execute(self.sql_text)
        result = cur.fetchall()
        return "数据库查询结果：\n{}".format(result)
