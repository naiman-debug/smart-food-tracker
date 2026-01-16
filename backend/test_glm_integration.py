"""
测试GLM API集成
验证API密钥和图像识别功能
"""
import os
import asyncio
import httpx
import base64

# 测试API密钥
GLM_API_KEY = "7ce400cc79454af49b6fd62ebc69e7ab.LiscGibdoY1Dzp4z"
GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
GLM_MODEL = "glm-4.6v-flash"


async def test_glm_api_key():
    """测试API密钥是否有效"""
    print("=" * 60)
    print("测试1: 验证API密钥")
    print("=" * 60)

    headers = {
        "Authorization": f"Bearer {GLM_API_KEY}",
        "Content-Type": "application/json"
    }

    # 简单文本测试
    payload = {
        "model": GLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": "你好，请回复'连接成功'"
            }
        ],
        "max_tokens": 50
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GLM_API_URL,
                headers=headers,
                json=payload
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"✅ API密钥有效！")
                print(f"响应内容: {content}")
                return True
            else:
                print(f"❌ API调用失败")
                print(f"响应内容: {response.text}")
                return False

    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        return False


async def test_image_recognition():
    """测试图像识别功能"""
    print("\n" + "=" * 60)
    print("测试2: 图像识别功能（使用模拟base64图片）")
    print("=" * 60)

    # 创建一个简单的测试图片（1x1像素红色PNG的base64）
    # 实际使用时应该用真实食物图片的base64
    test_image_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

    headers = {
        "Authorization": f"Bearer {GLM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GLM_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": test_image_base64
                        }
                    },
                    {
                        "type": "text",
                        "text": """请识别这张图片中的食物，只回答食物的名称，不要添加任何其他描述。
要求：
1. 只返回最主食/主菜的食物名称
2. 名称要简洁，如：鸡胸肉、米饭、鸡蛋
3. 不要回答烹饪方式或口感描述"""
                    }
                ]
            }
        ],
        "temperature": 0.3,
        "max_tokens": 50
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GLM_API_URL,
                headers=headers,
                json=payload
            )

            print(f"状态码: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                print(f"✅ 图像识别成功！")
                print(f"识别结果: {content}")

                # 测试食物名称标准化
                raw_name = content.strip().strip("。""，""、"".")
                print(f"标准化名称: {raw_name}")
                return True
            else:
                print(f"❌ 图像识别失败")
                print(f"响应内容: {response.text}")
                return False

    except Exception as e:
        print(f"❌ 连接错误: {str(e)}")
        return False


async def test_food_name_mapping():
    """测试食物名称映射功能"""
    print("\n" + "=" * 60)
    print("测试3: 食物名称映射功能")
    print("=" * 60)

    # 导入映射字典（模拟ai_service.py中的映射）
    FOOD_NAME_MAPPING = {
        # 鸡肉类
        "鸡胸肉": "鸡胸肉",
        "鸡肉": "鸡胸肉",
        "白切鸡": "鸡胸肉",
        "宫保鸡丁": "鸡胸肉",
        # ... 更多映射
    }

    test_cases = [
        ("宫保鸡丁", "鸡胸肉"),
        ("白切鸡", "鸡胸肉"),
        ("水煮蛋", "鸡蛋"),
        ("红烧肉", "红烧肉"),
    ]

    for raw, expected in test_cases:
        # 模拟normalize_food_name逻辑
        name = raw.strip().replace("，", "").replace("。", "")
        if name in FOOD_NAME_MAPPING:
            mapped = FOOD_NAME_MAPPING[name]
        else:
            mapped = name  # 无法映射

        status = "✅" if mapped == expected else "❌"
        print(f"{status} '{raw}' -> '{mapped}' (期望: '{expected}')")


async def main():
    """运行所有测试"""
    print("\n🔑 GLM API 集成测试")
    print(f"API密钥: {GLM_API_KEY[:10]}...")
    print(f"API模型: {GLM_MODEL}")
    print()

    results = []

    # 测试1: API密钥验证
    results.append(await test_glm_api_key())

    # 测试2: 图像识别
    results.append(await test_image_recognition())

    # 测试3: 名称映射
    await test_food_name_mapping()

    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"API密钥验证: {'✅ 通过' if results[0] else '❌ 失败'}")
    print(f"图像识别功能: {'✅ 通过' if results[1] else '❌ 失败'}")

    if all(results):
        print("\n🎉 所有测试通过！GLM集成工作正常。")
    else:
        print("\n⚠️  部分测试失败，请检查配置。")

    return all(results)


if __name__ == "__main__":
    asyncio.run(main())
