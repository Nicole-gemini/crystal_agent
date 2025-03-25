# test_wuxing.py
from agent import MysticRouterAgent

if __name__ == "__main__":
    agent = MysticRouterAgent()
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个有用的小助手。请调用下面的工具，始终使用中文回答用户的问题，"
                "并参考工具输出，推荐1到3个合适的水晶饰品。"
            )
        },
        {
            "role": "user",
            "content": (
                "我是张三，男，1987年7月7日17时17分17秒出生，"
                "想知道我的五行属性和破太岁的水晶饰品。"
            )
        }
    ]

    answer = agent.run(messages)
    print("五行测试场景的最终回答: ", answer)
