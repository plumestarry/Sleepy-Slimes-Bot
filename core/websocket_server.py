# core/websocket_server.py
import asyncio
import websockets
import json
import logging
from commands.whitelist import WhiteList
from typing import Callable
from config import settings
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment

class WebSocketServer:
    """异步WebSocket服务端"""
    def __init__(self, message_callback: Callable):
        self.server = None
        self.active_connections = set()
        self.message_callback = message_callback

    async def _handle_connection(self, websocket: websockets.ServerConnection):
        """处理单个WebSocket连接"""
        self.active_connections.add(websocket)
        try:
            settings.WebSocketsConfig.SOCKET = websocket
            await self._group_list()
            async for message in websocket:
                asyncio.create_task(self.message_callback(message, websocket, WhiteList.special_manage()))
        except websockets.ConnectionClosed:
            logging.warning("客户端连接异常关闭")
        finally:
            self.active_connections.remove(websocket)

    async def start(self):
        """启动WebSocket服务"""
        config = self._load_config()
        self.server = await websockets.serve(
            self._handle_connection,
            "localhost",
            config['port']
        )
        logging.info(f"WebSocket服务已启动，端口：{config['port']}")

    def _load_config(self):
        """加载配置文件"""
        with open(settings.PathConfig.CONFIG_JSON) as f:
            return json.load(f)['websocket']
    
    async def _group_list(self):
        """发送群组消息"""
        message_send_init = Message_SendFormat("send_group_msg", "group_id", 0).normal_message("Onebot_Mod Ver-0.6 Launch success!")
        for group_id in WhiteList.special_manage()["special"]:
            message_send_init["params"]["group_id"] = group_id
            await settings.WebSocketsConfig.SOCKET.send(json.dumps(message_send_init))