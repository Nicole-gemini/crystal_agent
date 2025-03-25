import os
import json
from openai import OpenAI
from typing import Sequence
import requests
import urllib
import urllib.request
import base64
import re
import urllib, urllib3, sys, uuid
import ssl

os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "0"


def get_wuxing_information(keyword:dict):
    """通过阿里云市场的命理玄学知识图谱-八字命运精批算命-艾科瑞特（iCREDIT）API，查询用户的五行属性"""
    host = 'https://xuanxue.market.alicloudapi.com'
    path = '/ai_china_knowledge/bazi/v1'
    #阿里云APPCODE：请替换成自己的APPCODE
    appcode = '' # 如果没有appcode，可以在阿里云市场申请
    url = host + path 
    querys = ""
    #参数配置
    # keyword = {
    #     "FIRST_NAME": "张",
    #     "SECOND_NAME": "三",
    #     "BIRTH": "19870707171717",
    #     "GENDER": "男"
    # }
    # 拼接参数，得到请求URL
    for key,value in keyword.items():
        if re.match(r'.*[\u4e00-\u9fa5]',value):
            value = urllib.request.quote(value)
        querys += key + "=" + value + "&"    

    url += "?" + querys[:-1]
    request = urllib.request.Request(url)
    request.add_header('Authorization', 'APPCODE ' + appcode)
    request.add_header('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8')

    # 发送请求
    response = urllib.request.urlopen(request)
    content = response.read()
    if (content):
        new_content=eval(content.decode('utf-8'))
        return f"五行分析: {new_content["命主八字命盘实体信息"]["命主八字实体信息五行分析"]["五行分析解读"]}"



def get_aztro_information(keyword:dict):
    """通过阿里云市场的星座运势API，查询用户的星座运势"""
    host = 'https://ali-star-lucky.showapi.com'
    path = '/star'
    method = 'GET'
    appcode = '6a246211b124486d952d71c5ba549a30'
    querys = ''
    # 让星座名称和API中的星座名称对应，方便调用，符合日常使用习惯
    sign_map={
        "白羊座":"baiyang",
        "金牛座":"jinniu",
        "双子座":"shuangzi",
        "巨蟹座":"juxie",
        "狮子座":"shizi",
        "处女座":"chunv",
        "天秤座":"tiancheng",
        "天蝎座":"tianxie",
        "射手座":"sheshou",
        "摩羯座":"mojie",
        "水瓶座":"shuiping",
        "双鱼座":"shuangyu"}
    #参数配置
    # keyword = {
    #     "star": "双子座" # 星座名称

    # }
    # 拼接参数，得到请求URL
    keyword["star"] = sign_map[keyword["star"]]
    # 查询年度运势
    querys = f'needMonth=0&star={keyword["star"]}&needWeek=0&needTomorrow=0&needYear=1'
    url = host + path + '?' + querys
    http = urllib3.PoolManager()
    headers = {
        'Authorization': 'APPCODE ' + appcode
    }
    response = http.request('GET', url, headers=headers)
    content = response.data.decode('utf-8')
    if (content):
        new_content=eval(content)
        return f"星座运势: {new_content["showapi_res_body"]["year"]["general_txt"]}"

def get_tarot_information(keyword:dict):
    """通过TarotAPI，查询22张大阿卡纳牌的相关信息，获知用户的重要的生命课题和精神成长"""
    # 通过塔罗牌的名称映射，得到对应的缩写名称，让没有使用过塔罗牌的用户方便调用api
    name_map = {
        "The Fool": "ar00",
        "The Magician": "ar01",
        "The High Priestess": "ar02",
        "The Empress": "ar03",
        "The Emperor": "ar04",
        "The Hierophant": "ar05",
        "The Lovers": "ar06",
        "The Chariot": "ar07",
        "Fortitude": "ar08",
        "The Hermit": "ar09",
        "Wheel of Fortune": "ar10",
        "Justice": "ar11",
        'The Hanged Man': "ar12",
        "Death": "ar13",
        "Temperance": "ar14",
        "The Devil": "ar15",
        "The Tower": "ar16",
        "The Star": "ar17",
        "The Moon": "ar18",
        "The Sun": "ar19",
        "The Last Judgment": "ar20",
        "The World": "ar21"
    }
    name_short = name_map[keyword['name']]
    url = f"https://tarotapi.dev/api/v1/cards/{name_short}"
    response = requests.get(url)
    response.raise_for_status()  # 检查请求是否成功
    cards = response.json()
    # 
    return f"抽取的塔罗牌的正位含义: {cards['card']['meaning_up']}, 抽取的塔罗牌的负位含义：{cards['card']['meaning_rev']}"


tool_map = {"get_wuxing_information": get_wuxing_information,
            "get_aztro_information": get_aztro_information,
            "get_tarot_information": get_tarot_information}


# def clean_output(text):
#     """清理乱码内容"""
#     # 由于刚开始lora训练模型时序列长度限制成512，文本内容出现乱码，需要清理
#     # 检测泰语起始符或JSON起始符
#     pattern = r'([\u0E00-\u0E7F\u4E00-\u9FFF]|โ|ฏ|ฑ).*?\{|{'
#     match = re.search(pattern, text)
#     if match:
#         return text[:match.start()]

#     reversed_text = text[::-1]
#     end_search = pattern.search(reversed_text)
#     if end_search:
#         # 计算正向截断位置
#         end_pos = len(text) - end_search.start()
#         text = text[:end_pos]
#     return text
if __name__ == "__main__":
    client = OpenAI()
    tools = [
        {
            "type": "function",
            "function": {
                            "name": "get_wuxing_information",
                            "description": "根据用户提供的姓名、性别、出生年月日时分秒信息，对用户的五行进行分析，推荐符合五行的水晶。",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "keyword": {
                                        "type":"dict",
                                        "description": "五行分析",
                                    },
                                },
                                "required": ["keyword"],
                            }
                        }
        },
        {
            "type": "function",
            "function": {
                            "name": "get_aztro_information",
                            "description": "根据用户提供的星座名称，查询星座年度运势，推荐能提升运势、克服水逆的水晶。",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "keyword": {
                                        "type":"dict",
                                        "description": "星座年度运势",
                                    },
                                },
                                "required": ["keyword"],
                            }
                        }
        },
        {
            "type": "function",
            "function": {
                            "name": "get_tarot_information",
                            "description": "根据用户抽取的塔罗牌名称，查询塔罗牌的正位和负位含义，推荐提升正位能量、降低负位影响的水晶。",
                            "parameters": {
                                "type": "object",
                                "properties": {
                                    "keyword": {
                                        "type":"dict",
                                        "description": "塔罗牌含义",
                                    },
                                },
                                "required": ["keyword"],
                            }
                        }
        }
    ]

    messages = []
    messages.append({"role": "system", "content": "你是一个有用的小助手，请调用工具，参考工具输出，推荐1到3个合适的水晶饰品。请始终使用简体中文进行回复。"})
    #messages.append({"role": "user", "content": "我是张三，男，1987年7月7日17时17分17秒出生，想知道我的五行属性和破太岁的水晶饰品。"})
    #messages.append({"role": "user", "content": "我是双子座，想知道我的星座运势和提升运势的水晶。"})
    #messages.append({"role": "user", "content": "我抽取了The Fool塔罗牌，想知道正位和负位的含义，以及提升正位能量的水晶。"})
    messages.append({"role": "user", "content": "我是金牛座，我要买幸运水晶。"})
    result = client.chat.completions.create(messages=messages, model="gpt-4o", tools=tools,max_tokens=512,temperature=0.2, )
    # 如果出现乱码的话，可以使用下面的代码进行清理
    # result.choices[0].message.content=clean_output(result.choices[0].message.content)
    func_call = result.choices[0].message.tool_calls[0].function
    name, args = func_call.name, json.loads(func_call.arguments)
    messages.append({"role": "function", "content": json.dumps({"name": name, "arguments": args}, ensure_ascii=False)})
    func_result = tool_map[name](**args)
    messages.append({"role": "tool", "content": "工具输出结果为: " + func_result})
    result = client.chat.completions.create(messages=messages, model="gpt-4o")
    print("Answer: ", result.choices[0].message.content)
