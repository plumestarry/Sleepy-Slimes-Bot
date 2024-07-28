from selenium import webdriver
from selenium.webdriver.edge.service import Service
import re
import json
from function.message_sendformat import Message_SendFormat, Parameter_Judgment

def msedgedriver(url, sessdata):
    
    # 启动Edge浏览器
    service = Service("static/msedgedriver.exe")
    options = webdriver.EdgeOptions()
    options.use_chromium = True
    
    driver = webdriver.Edge(service=service, options=options)
    
    driver.get(url)
    driver.add_cookie({"name": "SESSDATA", "value": "{}".format(sessdata)})
    driver.get(url)
    
    page_source = driver.page_source
    
    driver.quit()
    
    return page_source

def bilibili_sessdata():
    
    key = open("database/sessdata.txt", "r", encoding="utf-8")
    sessdata = key.readline()
    key.close()
    
    return sessdata.strip("\n")

def str_to_dict(source_data):
    
    # 正则表达式匹配div标签，隐藏属性为true，以及其内的内容
    div_pattern = r'<div hidden="true">([^<]+)</div>'
    matches = re.findall(div_pattern, source_data)

    # 将匹配到的字符串列表转换为JSON格式
    # 假设每个div的内容都是完整的JSON格式的字符串
    json_str_list = [json.dumps(match.strip()) for match in matches]

    # 将JSON字符串转换为字典
    dict_list = [json.loads(json_str) for json_str in json_str_list]

    return json.loads(dict_list[0])

def bilibili_search(keyword):
    
    url = "https://api.bilibili.com/x/web-interface/search/all/v2?keyword={}".format(keyword)
    
    source_data = msedgedriver(url, bilibili_sessdata())
    source_dict = str_to_dict(source_data)
    
    video_data = []
    video_content = []
    
    for dict_type in source_dict["data"]["result"]:
        if dict_type["result_type"] == "video":
            video_data = dict_type["data"]
            break
    
    count = 0
    dict_list = Message_SendFormat(0, 0, 0)
    for video_dict in video_data:

        # 使用re.sub函数替换匹配到的内容
        video_title = re.sub(r'<em class="keyword">([^<]+)</em>', r'\1', video_dict["title"])
        
        video_content.append(dict_list.image_text("https:" + video_dict["pic"]))
        video_content.append(dict_list.normal_text("\n标题：" + video_title + "\n播放量：" + str(video_dict["play"]) + "\n时长：" + video_dict["duration"] + "\nbv号：" + video_dict["bvid"] + "\n\n"))
        
        count += 1
        
        if count == 5:
            break
    
    
    return video_content

def bilibili_view(bvid):
    
    url = "https://api.bilibili.com/x/web-interface/view?bvid={}".format(bvid)
    
    source_data = msedgedriver(url, bilibili_sessdata())
    source_dict = str_to_dict(source_data)
    
    dict_list = Message_SendFormat(0, 0, 0)
    video_content = []
    
    video_dict = source_dict["data"]
    video_content.append(dict_list.image_text(video_dict["pic"]))
    video_content.append(dict_list.normal_text("\n\n标题：" + video_dict["title"] + "\n作者：" + video_dict["owner"]["name"] + "\n播放量：" + str(video_dict["stat"]["view"]) + "\n时长：" + str(video_dict["duration"]) + "\n点赞：" + str(video_dict["stat"]["like"]) + "\n投币：" + str(video_dict["stat"]["coin"]) + "\n收藏：" + str(video_dict["stat"]["favorite"]) + "\n链接：https://www.bilibili.com/video/" + bvid))

    return video_content


def bilibili_message(message_dict, message_text):
    
    user_list = Parameter_Judgment().parameter_judgment(message_dict)
    message = Message_SendFormat(user_list[0], user_list[1], user_list[2])
    
    if message_text[:2] == "BV":
        return message.text_framework(bilibili_view(message_text))
    
    return message.text_framework(bilibili_search(message_text))

    
    