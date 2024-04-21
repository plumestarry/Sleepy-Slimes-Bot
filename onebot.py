import asyncio
import websockets
import json
import time

async def handle_message(websocket, path):
    
    # 监听JSON数据流
    async for message in websocket:
        
        message = str(message)
        
        # 获得当前时间
        t = time.localtime()
        print(f"{t.tm_hour}-{t.tm_min}-{t.tm_sec}")
        
        # 如果没有消息或者消息出错则执行下一个循环
        if not message:
            continue
        if message[11:17] == "failed":
            continue
        
        # Unicode编码转Utf-8
        message = message.encode('utf-8')
        message = message.decode("unicode_escape")
        
        # 保存消息到JSON文件
        if message[2:10] != "interval":
            with open("received_messages.json", "a", encoding="utf-8") as file:
                file.write(message + "," + "\n")
        
        # JSON字符串转换为字典格式送去加工
        message_dict = json.loads(message)
        
        # 调用加工所要的方法
        # message_send = method(message_dict)
        
        # 返回加工后的字符串（以下字符串仅为举例）
        message_send = '{"action": "send_private_msg","params": {"user_id": 114514,"message": "你好"},"echo": "123"}'

        # 如果有值则发送字符串
        if message_send:
            await websocket.send(message_send)
  
        # 设置每处理1000条消息就暂停0.1秒
        if t.tm_min == 59 and round(t.tm_sec / 5) == 6:
            await asyncio.sleep(0.5)
        
        # 每天凌晨4点清空消息数据
        if t.tm_hour == 4 and t.tm_min == 0 and t.tm_sec < 10:
            with open("received_messages.json", "w", encoding="utf-8") as file:
                file.write("[" + "\n")

if __name__ == "__main__":
    
    # 在指定端口开启WebSocket服务
    start_server = websockets.serve(handle_message, "127.0.0.1", 5140)

    # 进入主循环
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
