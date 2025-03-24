# agent.py
import json
from openai import OpenAI
from tool_registry import TOOL_REGISTRY

class MysticRouterAgent:
    """
    此处实现一个简单的“混合路由Agent”：
    - 收集已注册的玄学工具，统一交给GPT-3.5-turbo模型
    - 根据对话模型的回答决定调用哪个工具以及传入的参数
    - 获取工具执行结果后再让模型产出最终答案
    """
    def __init__(self):
        # 初始化客户端与工具列表
        self.client = OpenAI()
        self.tools = []
        for _, tool_info in TOOL_REGISTRY.items():
            self.tools.append({
                "type": "function",
                "function": tool_info["function"]
            })

    def run(self, messages):
        """
        执行对话流程：
          1. 让GPT-3.5-turbo根据上下文自动选择并调用工具
          2. 拦截工具调用请求，执行对应的玄学函数
          3. 将工具结果插回对话，获取最终回答
        """
        # 第一次对话：让GPT基于用户问题选择工具
        result = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo",
            tools=self.tools
        )
        tool_call = result.choices[0].message.tool_calls[0].function
        tool_name = tool_call.name
        tool_args = json.loads(tool_call.arguments)

        # 执行工具函数
        tool_callable = TOOL_REGISTRY[tool_name]["callable"]
        tool_result = tool_callable(**tool_args)

        # 将工具执行结果注入后续对话
        messages.append({
            "role": "tool",
            "content": f"工具输出结果为: {tool_result}"
        })

        # 第二次对话：让GPT基于工具执行结果输出最终答案
        final_result = self.client.chat.completions.create(
            messages=messages,
            model="gpt-3.5-turbo"
        )
        return final_result.choices[0].message.content
