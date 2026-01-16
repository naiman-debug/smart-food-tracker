"""
应用常量配置 - 每日营养目标
"""
from typing import Dict, List
from datetime import datetime

# 每日营养目标（固定值，不存储在数据库中）
TARGET_DAILY_CALORIES = 2000  # kcal
TARGET_DAILY_PROTEIN = 60      # g


# 食物知识库初始化数据
FOOD_SEED_DATA: List[Dict] = [
    {
        "name": "米饭",
        "base_calories_per_100g": 130,
        "base_protein_per_100g": 2.7,
        "visual_portions": [
            {"portion_name": "半碗", "estimated_weight_grams": 100},
            {"portion_name": "一拳", "estimated_weight_grams": 150},
            {"portion_name": "一小碗", "estimated_weight_grams": 200},
        ]
    },
    {
        "name": "苹果",
        "base_calories_per_100g": 52,
        "base_protein_per_100g": 0.3,
        "visual_portions": [
            {"portion_name": "半个", "estimated_weight_grams": 100},
            {"portion_name": "一个", "estimated_weight_grams": 200},
            {"portion_name": "大个", "estimated_weight_grams": 250},
        ]
    },
    {
        "name": "鸡蛋",
        "base_calories_per_100g": 143,
        "base_protein_per_100g": 12.6,
        "visual_portions": [
            {"portion_name": "一个", "estimated_weight_grams": 50},
            {"portion_name": "两个", "estimated_weight_grams": 100},
        ]
    },
    {
        "name": "红烧肉",
        "base_calories_per_100g": 320,
        "base_protein_per_100g": 15,
        "visual_portions": [
            {"portion_name": "几块", "estimated_weight_grams": 80},
            {"portion_name": "一盘", "estimated_weight_grams": 150},
            {"portion_name": "满满一碗", "estimated_weight_grams": 200},
        ]
    },
    {
        "name": "青菜",
        "base_calories_per_100g": 25,
        "base_protein_per_100g": 2.0,
        "visual_portions": [
            {"portion_name": "一小份", "estimated_weight_grams": 80},
            {"portion_name": "一捧", "estimated_weight_grams": 120},
            {"portion_name": "满满一盘", "estimated_weight_grams": 200},
        ]
    },
]


def get_time_of_day() -> str:
    """根据当前时间返回时段"""
    hour = datetime.now().hour
    if 5 <= hour < 10:
        return "早晨"
    elif 10 <= hour < 14:
        return "中午"
    elif 14 <= hour < 17:
        return "下午"
    elif 17 <= hour < 21:
        return "晚上"
    else:
        return "深夜"
