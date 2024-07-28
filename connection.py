import asyncio
import websockets
import json
import time

from message_judgment import Basic_Judgment
from function.message_sendformat import Message_SendFormat
from function.database import OnebotDatabase

async def handle_message(websocket: websockets.WebSocketServerProtocol, path: str) -> None:
    
    manage_dict = special_manage()
    time_message = ""
    
    # with open("time.txt", "r", encoding="utf-8") as file:
    #     history_time = file.readline()
    #     if history_time:
    #         time_message += "\n重启时间:{:.2f}s".format(time.time() - float(history_time))
    #         print(time_message)
    # with open("time.txt", "w", encoding="utf-8") as file:
    #     pass

    # 初始化消息发送
    try:
        message_send_init = Message_SendFormat("send_group_msg", "group_id", 0).normal_message("Onebot_Mod Ver-0.5 Launch success!{}".format(time_message))
        for group_id in manage_dict["special"]:
            message_send_init["params"]["group_id"] = group_id
            await websocket.send(json.dumps(message_send_init))
    except Exception as e:
        with open("TackBack.txt", "a", encoding="utf-8") as file:
            file.write(str(e) + "初始化消息发送失败" + "\n")

    # 监听JSON数据流
    async for message in websocket:
        
        # 获得当前时间
        t = time.localtime()

        # 如果没有消息或者消息出错则执行下一个循环

        if not message or message[11:17] == "failed":
            continue
        
        # 保存消息到JSON文件
        if message[-22:-1] == '"post_type":"message"' or message[-21:-1] == '"post_type":"notice"':
            
            # print(message)
            
            message_send = ""
            message_dict = {}
        
            # JSON字符串转换为字典格式送去加工
            try:
                message_dict = json.loads(message)
            except Exception as e:
                with open("TackBack.txt", "a", encoding="utf-8") as file:
                    file.write(str(e) + "JSON 字符串转换为字典失败" + "\n")

            # 调用加工所要的方法
            try:
                message_send = Basic_Judgment().function_selection(message_dict, message_dict["post_type"], manage_dict)
            except Exception as e:
                with open("TackBack.txt", "a", encoding="utf-8") as file:
                    file.write(str(e) + "调用加工所要的方法失败" + "\n")

            # 如果有值则发送字符串
            if message_send:
                print(message_send)
                await websocket.send(json.dumps(message_send))
                
            # 记录消息数据             
            asyncio.create_task(save_message(message))
            
            continue
        
        # 每天凌晨4点清空消息数据
        if t.tm_hour == 4 and t.tm_min == 1:
            
            try:
                message_send_init = Message_SendFormat("send_group_msg", "group_id", 0).normal_message("呀~ 已经凌晨4点了呢~ 机器人也要睡一分钟哦~ 晚安喵~")
                for group_id in manage_dict["special"]:
                    message_send_init["params"]["group_id"] = group_id
                    await websocket.send(json.dumps(message_send_init))
                with open("received_messages.json", "w", encoding="utf-8") as file:
                    file.write("[" + "\n")
            except Exception as e:
                with open("TackBack.txt", "a", encoding="utf-8") as file:
                    file.write(str(e) + "清空消息数据失败" + "\n")

            await asyncio.sleep(60)

async def save_message(message: str) -> None:
    
    try:
        message = message.encode("utf-8")
        message = message.decode("utf-8")
        with open("received_messages.json", "a", encoding="utf-8") as file:
            file.write(message + "," + "\n")
    except Exception as e:
        with open("TackBack.txt", "a", encoding="utf-8") as file:
            file.write(str(e) + "Unicode 编码转 Utf-8 失败" + "\n")
            
def special_manage() -> dict[str, list[int]]:
    
    manage_dict = {}
    
    database = OnebotDatabase("database")
    con, cur = database("special_manage.db")
    
    manage_dict["special"] = []
    
    for group_id in database.get_data(con, cur, "group_id", "special"):
        manage_dict["special"].append(group_id[0])
        
    
    manage_dict["private"] = []
    
    for user_id in database.get_data(con, cur, "user_id", "private"):
        manage_dict["private"].append(user_id[0])
        
    database.close(con, cur)
    
    return manage_dict
