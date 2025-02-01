from function.message_sendformat import Message_SendFormat, Parameter_Judgment
import random
import requests

def random_image(message_dict):
    
    image_1 = "https://moe.jitsu.top/api" # ✓
    image_2 = "https://www.dmoe.cc/random.php" # ✓
    image_3 = "https://api.suyanw.cn/api/comic.php" # ✓
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    return message.image_message(random.choice([image_1, image_2, image_3]))

def key_image(message_dict, tag):
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    
    try:
        if tag[2] == "1":
            url = "https://api.lolicon.app/setu/v2?size=original&tag={}".format(tag[4:])
            response = requests.get(url)
        if tag[2] == "2":
            url = "https://api.lolicon.app/setu/v2?size=original&tag={}&proxy=pixiv.linkpc.net".format(tag[4:])
            response = requests.get(url)
        if response.ok:
            try:
                json_image = response.json()
                image = json_image['data'][0]['urls']['original']
            except Exception:
                return message.normal_message("未能查询到")
            return message.image_message(image)
        if tag[2] == "3":
            return message.image_message("https://sex.nyan.xyz/api/v2/img?tag={}".format(tag[4:]))
            
                
    except Exception as e:
        with open("TackBack.txt", "a", encoding="utf-8") as file:
            file.write(str(e) + "调用p站方法失败" + "\n")
            
    return message.normal_message("请求失败")
