# 核心功能集成验证测试脚本
# 用于验证智能食物记录App的核心功能

import sys
import os
import asyncio
import httpx
import json
from typing import Dict, Any

# API配置
API_BASE_URL = "http://localhost:8000/api"
TEST_IMAGE_BASE64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="


class Colors:
    """终端颜色"""
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(title: str):
    """打印标题"""
    print(f"\n{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{title}{Colors.RESET}")
    print(f"{Colors.BLUE}{Colors.BOLD}{'='*60}{Colors.RESET}\n")


def print_test(test_name: str, status: str, details: str = ""):
    """打印测试结果"""
    if status == "PASS":
        print(f"{Colors.GREEN}✓{Colors.RESET} {test_name}")
    elif status == "FAIL":
        print(f"{Colors.RED}✗{Colors.RESET} {test_name}")
    else:
        print(f"{Colors.YELLOW}○{Colors.RESET} {test_name}")
    if details:
        print(f"  {details}")


async def test_1_smart_suggestions():
    """测试1：智能建议与快速记录闭环"""
    print_header("测试1：智能建议与快速记录闭环")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # 步骤1：获取余额和建议
        print(f"{Colors.BOLD}步骤1：获取余额和建议{Colors.RESET}")
        response = await client.get(f"{API_BASE_URL}/balance")

        if response.status_code != 200:
            print_test("获取余额", "FAIL", f"状态码: {response.status_code}")
            return False

        balance_data = response.json()
        print_test("获取余额", "PASS", f"剩余热量: {balance_data.get('remaining_calories', 0)} 大卡")

        suggestions = balance_data.get('suggestions', [])
        if not suggestions:
            print_test("智能建议", "FAIL", "未返回建议列表")
            return False

        print_test("智能建议", "PASS", f"返回 {len(suggestions)} 个建议")

        # 显示建议详情
        print(f"\n{Colors.BOLD}推荐食物：{Colors.RESET}")
        for i, suggestion in enumerate(suggestions[:3], 1):
            print(f"  {i}. {suggestion.get('food_name')} - {suggestion.get('calories')} 大卡")
            print(f"     理由: {suggestion.get('reason')}")

        # 步骤2：快速记录（选取第一个建议）
        first_suggestion = suggestions[0]
        portion_id = first_suggestion.get('id')

        print(f"\n{Colors.BOLD}步骤2：快速记录 - {first_suggestion.get('food_name')}{Colors.RESET}")
        quick_record_response = await client.post(
            f"{API_BASE_URL}/quick-record",
            json={"visual_portion_id": portion_id}
        )

        if quick_record_response.status_code != 200:
            print_test("快速记录", "FAIL", f"状态码: {quick_record_response.status_code}")
            return False

        record_data = quick_record_response.json()
        print_test("快速记录", "PASS", f"记录成功: {record_data.get('food_name')}")

        # 步骤3：验证余额刷新
        print(f"\n{Colors.BOLD}步骤3：验证余额刷新{Colors.RESET}")
        new_balance_response = await client.get(f"{API_BASE_URL}/balance")
        new_balance_data = new_balance_response.json()

        old_remaining = balance_data.get('remaining_calories', 0)
        new_remaining = new_balance_data.get('remaining_calories', 0)
        recorded_calories = record_data.get('calories', 0)

        if new_remaining < old_remaining:
            print_test("余额刷新", "PASS", f"余额减少: {old_remaining} → {new_remaining}")
            return True
        else:
            print_test("余额刷新", "FAIL", "余额未正确扣除")
            return False


async def test_2_multi_food_recognition():
    """测试2：多食物识别与添加流程"""
    print_header("测试2：多食物识别与添加流程")

    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"{Colors.BOLD}步骤1：调用多食物识别API{Colors.RESET}")

        response = await client.post(
            f"{API_BASE_URL}/analyze-multi",
            json={
                "image_base64": TEST_IMAGE_BASE64,
                "multi_food": True
            }
        )

        if response.status_code != 200:
            print_test("多食物识别API", "FAIL", f"状态码: {response.status_code}")
            print(f"  响应: {response.text}")
            return False

        data = response.json()
        foods = data.get('foods', [])
        ai_used = data.get('ai_used', False)

        print_test("多食物识别API", "PASS", f"识别到 {len(foods)} 种食物 (AI: {ai_used})")

        if not foods:
            print_test("返回食物列表", "FAIL", "未返回任何食物")
            return False

        print_test("返回食物列表", "PASS", f"食物: {[f.get('food_name') for f in foods]}")

        # 步骤2：验证每个食物的份量选项
        print(f"\n{Colors.BOLD}步骤2：验证份量选项{Colors.RESET}")
        all_portions_valid = True

        for food in foods:
            food_name = food.get('food_name')
            portions = food.get('portion_options', [])

            if not portions:
                print_test(f"{food_name} 份量选项", "FAIL", "无份量选项")
                all_portions_valid = False
                continue

            print_test(f"{food_name} 份量选项", "PASS", f"{len(portions)} 个选项")

            # 显示第一个份量选项
            if portions:
                first_portion = portions[0]
                print(f"    示例: {first_portion.get('portion_name')} - {first_portion.get('calories')} 大卡")

        return all_portions_valid


async def test_3_portion_options():
    """测试3：份量选项动态显示"""
    print_header("测试3：份量选项动态显示")

    # 测试数据：苹果（水果类）和鸡胸肉（肉类）
    test_foods = [
        {"name": "苹果", "expected_keyword": "网球大小", "category": "水果"},
        {"name": "鸡胸肉", "expected_keyword": "掌心大小", "category": "肉类"},
        {"name": "生菜沙拉", "expected_keyword": "双手一捧", "category": "蔬菜"},
        {"name": "米饭", "expected_keyword": "一小碗", "category": "主食"},
    ]

    async with httpx.AsyncClient(timeout=30.0) as client:
        all_pass = True

        for test_food in test_foods:
            food_name = test_food["name"]
            expected_keyword = test_food["expected_keyword"]
            category = test_food["category"]

            print(f"\n{Colors.BOLD}测试: {food_name} ({category}){Colors.RESET}")

            # 调用单食物识别API
            response = await client.post(
                f"{API_BASE_URL}/analyze",
                json={
                    "image_base64": TEST_IMAGE_BASE64,
                    "multi_food": False
                }
            )

            if response.status_code != 200:
                print_test(f"{food_name} 识别", "FAIL", f"状态码: {response.status_code}")
                all_pass = False
                continue

            data = response.json()
            portions = data.get('portion_options', [])

            if not portions:
                print_test(f"{food_name} 份量选项", "FAIL", "无份量选项")
                all_pass = False
                continue

            # 检查是否包含预期的关键词
            found_keyword = False
            portion_names = []
            for p in portions:
                portion_name = p.get('portion_name', '')
                portion_names.append(portion_name)
                if expected_keyword in portion_name:
                    found_keyword = True

            if found_keyword:
                print_test(f"{food_name} 份量描述", "PASS", f"包含「{expected_keyword}」")
                print(f"    所有选项: {', '.join(portion_names)}")
            else:
                print_test(f"{food_name} 份量描述", "FAIL", f"未包含「{expected_keyword}」")
                print(f"    实际选项: {', '.join(portion_names)}")
                all_pass = False

        return all_pass


async def run_all_tests():
    """运行所有测试"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════╗")
    print("║   智能食物记录 - 核心功能集成验证测试   ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    print(f"{Colors.YELLOW}注意: 请确保后端服务已启动 (uvicorn app.main:app --reload){Colors.RESET}\n")

    results = {}

    # 测试1：智能建议与快速记录
    try:
        results["test1"] = await test_1_smart_suggestions()
    except Exception as e:
        print_test("测试1", "FAIL", f"异常: {str(e)}")
        results["test1"] = False

    # 测试2：多食物识别
    try:
        results["test2"] = await test_2_multi_food_recognition()
    except Exception as e:
        print_test("测试2", "FAIL", f"异常: {str(e)}")
        results["test2"] = False

    # 测试3：份量选项动态显示
    try:
        results["test3"] = await test_3_portion_options()
    except Exception as e:
        print_test("测试3", "FAIL", f"异常: {str(e)}")
        results["test3"] = False

    # 打印总结
    print_header("测试总结")

    pass_count = sum(1 for v in results.values() if v)
    total_count = len(results)

    print(f"测试结果: {Colors.GREEN}{pass_count}/{total_count}{Colors.RESET} 通过")
    print()

    for test_name, passed in results.items():
        status = f"{Colors.GREEN}通过{Colors.RESET}" if passed else f"{Colors.RED}失败{Colors.RESET}"
        test_title = {
            "test1": "测试1：智能建议与快速记录闭环",
            "test2": "测试2：多食物识别与添加流程",
            "test3": "测试3：份量选项动态显示"
        }
        print(f"  {test_title[test_name]}: {status}")

    print()

    if all(results.values()):
        print(f"{Colors.GREEN}{Colors.BOLD}✓ 所有测试通过！{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}✗ 部分测试失败{Colors.RESET}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
