# config/constants.py
class EventType:
    MESSAGE = "message"
    NOTICE = "notice"
    META = "meta_event"

class ConnectionStatus:
    CONNECTED = "connected"
    DISCONNECTED = "disconnected"
    RECONNECTING = "reconnecting"