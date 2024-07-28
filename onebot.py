import asyncio
import websockets
from connection import handle_message

for i in range(2):
        
    try:
            
        print("Onebot_Mod Ver-0.5 Launch success!")
        port = 5140
        with open("database/port.txt", "r", encoding="utf-8") as file:
            port = file.readline()
        
        # 在指定端口开启WebSocket服务
        start_server = websockets.serve(handle_message, "127.0.0.1", port)
            
        # 进入主循环
        asyncio.get_event_loop().run_until_complete(start_server)
        asyncio.get_event_loop().run_forever()
        
        # 等待所有任务完成
        pending = asyncio.all_tasks(asyncio.get_event_loop())
        asyncio.get_event_loop().run_until_complete(asyncio.gather(*pending))
            
        # 清理当前的事件循环
        asyncio.get_event_loop().run_until_complete(asyncio.get_event_loop().shutdown_asyncgens())
        asyncio.get_event_loop().close()
        
        asyncio.set_event_loop(asyncio.new_event_loop())
            
    except Exception as e:
        with open("TackBack.txt", "a", encoding="utf-8") as file:
            file.write(str(e) + "循环失败" + "\n")
        
                
