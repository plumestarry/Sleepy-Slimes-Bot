
from commands.method.message_sendformat import Message_SendFormat, Parameter_Judgment
from commands.method.deepseek import DeepSeekAPI
from config import settings
import json
with open(settings.PathConfig.CONFIG_JSON) as f:
    temp = json.load(f)
    settings.DeepSeekConfig.API_KEY = temp['deepseek']['key']
    settings.DeepSeekConfig.API_URL = temp['deepseek']['url']

deepseek = DeepSeekAPI()
if __name__ == '__main__':
    deepseek.async_chat("你好", 0.0, "")