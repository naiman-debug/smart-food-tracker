"""
数据库初始化脚本 - VisualPortion 知识库
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models.database import SessionLocal, engine, Base
from app.models.visual_portion import VisualPortion
from app.models.daily_goal import DailyGoal


# 视觉份量知识库数据
# 每条记录 = 某种食物 + 某种视觉份量的完整营养定义
VISUAL_PORTIONS_DATA = [
    # 肉类 - 掌心大小
    {"food_name": "鸡胸肉", "portion_name": "掌心大小（薄切，约80g）", "weight_grams": 80, "calories_per_100g": 165, "protein_per_100g": 31},
    {"food_name": "鸡胸肉", "portion_name": "掌心大小（正常厚度，约120g）", "weight_grams": 120, "calories_per_100g": 165, "protein_per_100g": 31},
    {"food_name": "鸡胸肉", "portion_name": "掌心大小×1.5（厚切，约180g）", "weight_grams": 180, "calories_per_100g": 165, "protein_per_100g": 31},

    {"food_name": "牛肉", "portion_name": "信用卡厚度×掌心大小（约60g）", "weight_grams": 60, "calories_per_100g": 250, "protein_per_100g": 26},
    {"food_name": "牛肉", "portion_name": "掌心大小（约100g）", "weight_grams": 100, "calories_per_100g": 250, "protein_per_100g": 26},
    {"food_name": "牛肉", "portion_name": "掌心大小×1.5（约150g）", "weight_grams": 150, "calories_per_100g": 250, "protein_per_100g": 26},

    {"food_name": "猪肉", "portion_name": "掌心大小（薄切，约80g）", "weight_grams": 80, "calories_per_100g": 143, "protein_per_100g": 20},
    {"food_name": "猪肉", "portion_name": "掌心大小（正常厚度，约120g）", "weight_grams": 120, "calories_per_100g": 143, "protein_per_100g": 20},
    {"food_name": "猪肉", "portion_name": "掌心大小×1.5（厚切，约180g）", "weight_grams": 180, "calories_per_100g": 143, "protein_per_100g": 20},

    {"food_name": "红烧肉", "portion_name": "掌心大小（约3-4块，100g）", "weight_grams": 100, "calories_per_100g": 358, "protein_per_100g": 10},
    {"food_name": "红烧肉", "portion_name": "掌心大小×1.5（约5-6块，150g）", "weight_grams": 150, "calories_per_100g": 358, "protein_per_100g": 10},
    {"food_name": "红烧肉", "portion_name": "双掌心大小（约200g）", "weight_grams": 200, "calories_per_100g": 358, "protein_per_100g": 10},

    {"food_name": "鱼", "portion_name": "掌心大小（约100g）", "weight_grams": 100, "calories_per_100g": 140, "protein_per_100g": 25},
    {"food_name": "鱼", "portion_name": "掌心大小×1.5（约150g）", "weight_grams": 150, "calories_per_100g": 140, "protein_per_100g": 25},
    {"food_name": "鱼", "portion_name": "双掌心大小（约200g）", "weight_grams": 200, "calories_per_100g": 140, "protein_per_100g": 25},

    {"food_name": "虾", "portion_name": "一小把（约5-6只，80g）", "weight_grams": 80, "calories_per_100g": 99, "protein_per_100g": 24},
    {"food_name": "虾", "portion_name": "一大把（约10只，150g）", "weight_grams": 150, "calories_per_100g": 99, "protein_per_100g": 24},

    # 主食 - 碗
    {"food_name": "米饭", "portion_name": "半小碗（约50g）", "weight_grams": 50, "calories_per_100g": 130, "protein_per_100g": 2.7},
    {"food_name": "米饭", "portion_name": "一小碗（约100g）", "weight_grams": 100, "calories_per_100g": 130, "protein_per_100g": 2.7},
    {"food_name": "米饭", "portion_name": "平时饭碗的一碗半（约150g）", "weight_grams": 150, "calories_per_100g": 130, "protein_per_100g": 2.7},

    {"food_name": "面条", "portion_name": "半小碗（约50g）", "weight_grams": 50, "calories_per_100g": 110, "protein_per_100g": 4},
    {"food_name": "面条", "portion_name": "一小碗（约100g）", "weight_grams": 100, "calories_per_100g": 110, "protein_per_100g": 4},
    {"food_name": "面条", "portion_name": "平时饭碗的一碗半（约150g）", "weight_grams": 150, "calories_per_100g": 110, "protein_per_100g": 4},

    {"food_name": "馒头", "portion_name": "半个小馒头（约50g）", "weight_grams": 50, "calories_per_100g": 223, "protein_per_100g": 7},
    {"food_name": "馒头", "portion_name": "一个小馒头（约100g）", "weight_grams": 100, "calories_per_100g": 223, "protein_per_100g": 7},
    {"food_name": "馒头", "portion_name": "一个大馒头（约150g）", "weight_grams": 150, "calories_per_100g": 223, "protein_per_100g": 7},

    {"food_name": "全麦面包", "portion_name": "一片（约30g）", "weight_grams": 30, "calories_per_100g": 246, "protein_per_100g": 9},
    {"food_name": "全麦面包", "portion_name": "两片（约60g）", "weight_grams": 60, "calories_per_100g": 246, "protein_per_100g": 9},

    # 蔬菜 - 双手捧
    {"food_name": "青菜", "portion_name": "一手抓起的量（约30g）", "weight_grams": 30, "calories_per_100g": 25, "protein_per_100g": 2},
    {"food_name": "青菜", "portion_name": "双手一捧（约80g）", "weight_grams": 80, "calories_per_100g": 25, "protein_per_100g": 2},
    {"food_name": "青菜", "portion_name": "双手一捧×1.5（约120g）", "weight_grams": 120, "calories_per_100g": 25, "protein_per_100g": 2},

    {"food_name": "生菜沙拉", "portion_name": "一手抓起的量（约30g）", "weight_grams": 30, "calories_per_100g": 20, "protein_per_100g": 1.5},
    {"food_name": "生菜沙拉", "portion_name": "双手一捧（约80g）", "weight_grams": 80, "calories_per_100g": 20, "protein_per_100g": 1.5},
    {"food_name": "生菜沙拉", "portion_name": "双手一捧×1.5（约120g）", "weight_grams": 120, "calories_per_100g": 20, "protein_per_100g": 1.5},

    {"food_name": "西兰花", "portion_name": "一小朵（约50g）", "weight_grams": 50, "calories_per_100g": 34, "protein_per_100g": 2.8},
    {"food_name": "西兰花", "portion_name": "一大朵（约100g）", "weight_grams": 100, "calories_per_100g": 34, "protein_per_100g": 2.8},
    {"food_name": "西兰花", "portion_name": "满满一碗（约150g）", "weight_grams": 150, "calories_per_100g": 34, "protein_per_100g": 2.8},

    {"food_name": "番茄", "portion_name": "一个番茄（约100g）", "weight_grams": 100, "calories_per_100g": 18, "protein_per_100g": 0.9},
    {"food_name": "番茄", "portion_name": "两个番茄（约200g）", "weight_grams": 200, "calories_per_100g": 18, "protein_per_100g": 0.9},

    {"food_name": "黄瓜", "portion_name": "半根黄瓜（约80g）", "weight_grams": 80, "calories_per_100g": 16, "protein_per_100g": 0.8},
    {"food_name": "黄瓜", "portion_name": "一根黄瓜（约150g）", "weight_grams": 150, "calories_per_100g": 16, "protein_per_100g": 0.8},

    # 水果 - 拳头/网球
    {"food_name": "苹果", "portion_name": "网球大小（小苹果，约80g）", "weight_grams": 80, "calories_per_100g": 52, "protein_per_100g": 0.3},
    {"food_name": "苹果", "portion_name": "拳头大小（正常苹果，约150g）", "weight_grams": 150, "calories_per_100g": 52, "protein_per_100g": 0.3},
    {"food_name": "苹果", "portion_name": "拳头大小×1.5（大苹果，约225g）", "weight_grams": 225, "calories_per_100g": 52, "protein_per_100g": 0.3},

    {"food_name": "香蕉", "portion_name": "半根香蕉（约60g）", "weight_grams": 60, "calories_per_100g": 89, "protein_per_100g": 1.1},
    {"food_name": "香蕉", "portion_name": "一根香蕉（约120g）", "weight_grams": 120, "calories_per_100g": 89, "protein_per_100g": 1.1},

    {"food_name": "橙子", "portion_name": "网球大小（小橙子，约100g）", "weight_grams": 100, "calories_per_100g": 47, "protein_per_100g": 0.9},
    {"food_name": "橙子", "portion_name": "拳头大小（正常橙子，约180g）", "weight_grams": 180, "calories_per_100g": 47, "protein_per_100g": 0.9},

    {"food_name": "葡萄", "portion_name": "一小串（约80g）", "weight_grams": 80, "calories_per_100g": 69, "protein_per_100g": 0.7},
    {"food_name": "葡萄", "portion_name": "一大串（约150g）", "weight_grams": 150, "calories_per_100g": 69, "protein_per_100g": 0.7},

    # 蛋类 & 豆制品
    {"food_name": "鸡蛋", "portion_name": "一个水煮蛋（约50g）", "weight_grams": 50, "calories_per_100g": 155, "protein_per_100g": 13},
    {"food_name": "鸡蛋", "portion_name": "两个水煮蛋（约100g）", "weight_grams": 100, "calories_per_100g": 155, "protein_per_100g": 13},

    {"food_name": "豆腐", "portion_name": "一小块（约100g）", "weight_grams": 100, "calories_per_100g": 76, "protein_per_100g": 8},
    {"food_name": "豆腐", "portion_name": "一大块（约200g）", "weight_grams": 200, "calories_per_100g": 76, "protein_per_100g": 8},
]


def init_db():
    """初始化数据库"""
    print("正在创建数据库表...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db: Session = SessionLocal()
    try:
        print("正在创建视觉份量知识库...")
        for data in VISUAL_PORTIONS_DATA:
            portion = VisualPortion(**data)
            db.add(portion)

        # 创建示例目标
        print("正在创建示例用户目标...")
        example_goal = DailyGoal(
            gender="男",
            age=28,
            height_cm=175,
            weight_kg=70,
            deficit_target=-500
        )
        example_goal.calculate_targets()
        db.add(example_goal)

        db.commit()
        print("\n数据库初始化完成！")
        print(f"  - 视觉份量条目: {len(VISUAL_PORTIONS_DATA)}")
        print(f"  - 覆盖食物: {len(set(d['food_name'] for d in VISUAL_PORTIONS_DATA))} 种")

    except Exception as e:
        print(f"\n初始化失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
