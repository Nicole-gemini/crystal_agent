# 该文件定义了工具注册表，用于注册和管理所有工具函数，提供模块化注册功能。

import os
from typing import Dict, Any, Callable
from mystic_tools import get_wuxing_information, get_aztro_information, get_tarot_information

# 根据实际部署情况配置 OPENAI 环境变量
# 此处使用vllm部署的本地环境
os.environ["OPENAI_BASE_URL"] = "http://localhost:8000/v1"
os.environ["OPENAI_API_KEY"] = "0"

# 全局工具注册表：tool_name -> { "function": {...}, "callable": fn }
TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {}

def register_tool(
    name: str,
    description: str,
    parameters: Dict[str, Any],
    func: Callable
):
    """
    注册一个新玄学工具。
    :param name:           工具函数名称（对外暴露给对话模型）
    :param description:    工具功能描述（仅对话模型可见）
    :param parameters:     工具参数的 JSON Schema 定义
    :param func:           实际的可调用函数
    """
    TOOL_REGISTRY[name] = {
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": parameters
                },
                "required": ["keyword"],
            }
        },
        "callable": func
    }



# 模块化工具注册接口支持快速扩展新玄学场景
register_tool(
    name="get_wuxing_information",
    description="根据用户提供的姓名、性别、出生年月日时分秒信息，对用户的五行进行分析，推荐符合五行的水晶。",
    parameters={
        "FIRST_NAME": {"type": "string", "description": "姓氏"},
        "SECOND_NAME": {"type": "string", "description": "名字"},
        "BIRTH": {"type": "string", "description": "出生日期(YYYYMMDDHHMMSS)"},
        "GENDER": {"type": "string", "description": "性别: 男/女"}
    },
    func=get_wuxing_information
)

register_tool(
    name="get_aztro_information",
    description="根据用户提供的星座名称，查询星座年度运势，推荐能提升运势的水晶。",
    parameters={
       "star": {"type": "string", "description": "星座名称"}
    },
    func=get_aztro_information
)

register_tool(
    name="get_tarot_information",
    description="根据用户抽取的塔罗牌名称，查询塔罗牌的正位和负位含义，推荐对应水晶。",
    parameters={
        "name": {"type": "string", "description": "塔罗牌名称"} 
    },
    func=get_tarot_information
)
