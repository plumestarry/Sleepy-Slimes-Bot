# core/websocket_server.py
import asyncio
import websockets
import json
import logging
from typing import Callable
from config import constants, settings

class WebSocketServer:
    """异步WebSocket服务端"""
    def __init__(self, message_callback: Callable):
        self.server = None
        self.active_connections = set()
        self.message_callback = message_callback

    async def _handle_connection(self, websocket):
        """处理单个WebSocket连接"""
        self.active_connections.add(websocket)
        try:
            async for message in websocket:
                asyncio.create_task(self.message_callback(message))
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