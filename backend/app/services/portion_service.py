"""
视觉份量服务 - 根据食物类型提供对应的份量描述
符合PRD要求的视觉参照系统
"""
from typing import List, Dict
from sqlalchemy.orm import Session
from ..models.visual_portion import VisualPortion


class FoodCategory:
    """食物类别定义"""
    MEAT = "meat"           # 肉类/禽类/鱼类
    FRUIT = "fruit"         # 水果
    VEGETABLE = "vegetable" # 蔬菜
    STAPLE = "staple"       # 主食
    DAIRY = "dairy"         # 乳制品
    EGG = "egg"             # 蛋类
    OTHER = "other"         # 其他


class PortionService:
    """视觉份量服务"""

    # 食物名称到类别的映射
    FOOD_CATEGORY_MAP = {
        # 肉类/禽类/鱼类
        "鸡胸肉": FoodCategory.MEAT,
        "牛肉": FoodCategory.MEAT,
        "牛排": FoodCategory.MEAT,
        "红烧肉": FoodCategory.MEAT,
        "猪肉": FoodCategory.MEAT,
        "排骨": FoodCategory.MEAT,
        "五花肉": FoodCategory.MEAT,
        "鱼": FoodCategory.MEAT,
        "虾": FoodCategory.MEAT,

        # 水果
        "苹果": FoodCategory.FRUIT,
        "香蕉": FoodCategory.FRUIT,
        "橙子": FoodCategory.FRUIT,
        "葡萄": FoodCategory.FRUIT,

        # 蔬菜
        "生菜沙拉": FoodCategory.VEGETABLE,
        "青菜": FoodCategory.VEGETABLE,
        "菠菜": FoodCategory.VEGETABLE,
        "西兰花": FoodCategory.VEGETABLE,
        "白菜": FoodCategory.VEGETABLE,

        # 主食
        "米饭": FoodCategory.STAPLE,
        "面条": FoodCategory.STAPLE,
        "意大利面": FoodCategory.STAPLE,
        "全麦面包": FoodCategory.STAPLE,

        # 乳制品
        "牛奶": FoodCategory.DAIRY,
        "酸奶": FoodCategory.DAIRY,
        "奶酪": FoodCategory.DAIRY,

        # 蛋类
        "鸡蛋": FoodCategory.EGG,

        # 豆制品
        "豆腐": FoodCategory.OTHER,
        "豆浆": FoodCategory.OTHER,
    }

    # 各类别推荐的份量描述模式
    PORTION_PATTERNS = {
        FoodCategory.MEAT: [
            "掌心大小（薄切",
            "掌心大小（正常厚度",
            "掌心大小×1.5（厚切",
            "信用卡厚度",
        ],
        FoodCategory.FRUIT: [
            "网球大小",
            "拳头大小",
            "拳头大小×1.5",
        ],
        FoodCategory.VEGETABLE: [
            "一手抓起",
            "双手一捧",
            "双手一捧×1.5",
        ],
        FoodCategory.STAPLE: [
            "一小碗",
            "平时饭碗的一碗",
            "平时饭碗的一碗半",
        ],
        FoodCategory.DAIRY: [
            "一小杯",
            "一杯",
            "一大杯",
        ],
        FoodCategory.EGG: [
            "水煮蛋",
            "煎蛋",
        ],
        FoodCategory.OTHER: [
            "一小块",
            "正常份量",
            "大份量",
        ],
    }

    @classmethod
    def get_food_category(cls, food_name: str) -> str:
        """
        获取食物类别

        Args:
            food_name: 食物名称

        Returns:
            食物类别 (FoodCategory常量)
        """
        return cls.FOOD_CATEGORY_MAP.get(food_name, FoodCategory.OTHER)

    @classmethod
    def get_portion_options_for_food(cls, db: Session, food_name: str) -> List[Dict]:
        """
        获取指定食物的视觉份量选项
        按照PRD要求的顺序返回份量选项

        Args:
            db: 数据库会话
            food_name: 食物名称

        Returns:
            份量选项列表，按推荐顺序排列
        """
        # 获取食物类别
        category = cls.get_food_category(food_name)

        # 查询该食物的所有份量选项
        portions = db.query(VisualPortion).filter(
            VisualPortion.food_name == food_name
        ).all()

        if not portions:
            return []

        # 根据类别排序份量选项
        pattern_priority = cls.PORTION_PATTERNS.get(category, [])

        def sort_key(portion):
            """排序函数：根据份量描述模式匹配优先级"""
            portion_name = portion.portion_name
            for i, pattern in enumerate(pattern_priority):
                if pattern in portion_name:
                    return i
            return len(pattern_priority)  # 未匹配的模式排在最后

        sorted_portions = sorted(portions, key=sort_key)

        # 构建响应
        return [
            {
                "id": p.id,
                "food_name": p.food_name,
                "portion_name": p.portion_name,
                "weight_grams": p.weight_grams,
                "calories": p.get_calories(),
                "protein": p.get_protein(),
                "category": category
            }
            for p in sorted_portions
        ]

    @classmethod
    def get_portion_description_guide(cls, food_name: str) -> str:
        """
        获取份量选择指南

        根据PRD返回不同食物类别的份量描述说明
        """
        category = cls.get_food_category(food_name)

        guides = {
            FoodCategory.MEAT: "肉类份量参照：掌心大小（薄切/正常/厚切）或信用卡厚度",
            FoodCategory.FRUIT: "水果份量参照：网球大小或拳头大小",
            FoodCategory.VEGETABLE: "蔬菜份量参照：一手抓起或双手一捧",
            FoodCategory.STAPLE: "主食份量参照：一小碗或平时饭碗的一碗半",
            FoodCategory.DAIRY: "乳制品份量参照：一小杯或一杯",
            FoodCategory.EGG: "蛋类份量参照：水煮蛋或煎蛋",
            FoodCategory.OTHER: "份量参照：按正常食量估算",
        }

        return guides.get(category, "份量参照：按实际情况估算")


# 便捷函数
def get_portion_options(db: Session, food_name: str) -> List[Dict]:
    """
    便捷函数：获取食物份量选项
    """
    return PortionService.get_portion_options_for_food(db, food_name)


def get_food_category(food_name: str) -> str:
    """
    便捷函数：获取食物类别
    """
    return PortionService.get_food_category(food_name)
