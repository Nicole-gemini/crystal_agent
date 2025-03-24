# 实现五行属性、星座运势、塔罗牌的查询功能
# 通过调用外部API（阿里云市场的API、TarotAPI）实现

import os
import json
from typing import Sequence
import requests
import urllib
import urllib.request
import base64
import re
import urllib, urllib3, sys, uuid
import ssl


def get_wuxing_information(keyword:dict):
    """通过阿里云市场的命理玄学知识图谱-八字命运精批算命-艾科瑞特（iCREDIT）API，查询用户的五行属性"""
    host = 'https://xuanxue.market.alicloudapi.com'
    path = '/ai_china_knowledge/bazi/v1'
    #阿里云APPCODE
    appcode = '6a246211b124486d952d71c5ba549a30' 
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

