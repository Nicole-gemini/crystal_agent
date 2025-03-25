# test_aztro.py
# 测试脚本
from agent import MysticRouterAgent

if __name__ == "__main__":
    agent = MysticRouterAgent()
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个有用的小助手。请调用工具，始终使用中文回答用户的问题，"
                "并参考工具输出，推荐1到3个合适的水晶饰品。"
            )
        },
        {
            "role": "user",
            "content": (
                "我是双子座，想知道我的星座运势和提升运势的水晶。"
            )
        }
    ]

    answer = agent.run(messages)
    print("星座测试场景的最终回答: ", answer)
