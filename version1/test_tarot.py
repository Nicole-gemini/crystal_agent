# test_tarot.py
from agent import MysticRouterAgent

if __name__ == "__main__":
    agent = MysticRouterAgent()
    messages = [
        {
            "role": "system",
            "content": (
                "你是一个有用的小助手。请调用下面的工具回答用户的问题，"
                "并参考工具输出，推荐1到3个合适的水晶饰品。"
            )
        },
        {
            "role": "user",
            "content": (
                "我抽取了The Fool塔罗牌，想知道正位和负位含义，"
                "以及提升正位能量，降低负位影响的水晶。"
            )
        }
    ]

    answer = agent.run(messages)
    print("塔罗测试场景的最终回答: ", answer)
