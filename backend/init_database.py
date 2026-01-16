"""
数据库初始化脚本
填充 VisualPortion 表的食物份量数据
符合PRD要求的视觉参照系统
"""
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models.database import engine, Base, SessionLocal
from app.models.visual_portion import VisualPortion


# 食物份量数据 - 符合PRD要求
FOOD_PORTIONS_DATA = [
    # ========== 肉类/禽类/鱼类 ==========
    # 鸡胸肉 - 掌心大小参考
    {
        "food_name": "鸡胸肉",
        "portion_name": "掌心大小（薄切，约80g）",
        "weight_grams": 80,
        "calories_per_100g": 165,
        "protein_per_100g": 31
    },
    {
        "food_name": "鸡胸肉",
        "portion_name": "掌心大小（正常厚度，约120g）",
        "weight_grams": 120,
        "calories_per_100g": 165,
        "protein_per_100g": 31
    },
    {
        "food_name": "鸡胸肉",
        "portion_name": "掌心大小×1.5（厚切，约180g）",
        "weight_grams": 180,
        "calories_per_100g": 165,
        "protein_per_100g": 31
    },
    {
        "food_name": "鸡胸肉",
        "portion_name": "信用卡厚度（约50g）",
        "weight_grams": 50,
        "calories_per_100g": 165,
        "protein_per_100g": 31
    },

    # 牛肉
    {
        "food_name": "牛肉",
        "portion_name": "掌心大小（薄切，约80g）",
        "weight_grams": 80,
        "calories_per_100g": 250,
        "protein_per_100g": 26
    },
    {
        "food_name": "牛肉",
        "portion_name": "掌心大小（正常厚度，约120g）",
        "weight_grams": 120,
        "calories_per_100g": 250,
        "protein_per_100g": 26
    },

    # 牛排
    {
        "food_name": "牛排",
        "portion_name": "掌心大小（约150g）",
        "weight_grams": 150,
        "calories_per_100g": 271,
        "protein_per_100g": 25
    },

    # 红烧肉
    {
        "food_name": "红烧肉",
        "portion_name": "掌心大小（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 320,
        "protein_per_100g": 15
    },

    # 鱼类
    {
        "food_name": "鱼",
        "portion_name": "掌心大小（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 140,
        "protein_per_100g": 20
    },

    # 虾
    {
        "food_name": "虾",
        "portion_name": "一手抓（约80g）",
        "weight_grams": 80,
        "calories_per_100g": 85,
        "protein_per_100g": 20
    },

    # ========== 水果类 ==========
    # 苹果 - 拳头/网球大小参考
    {
        "food_name": "苹果",
        "portion_name": "网球大小（小苹果，约80g）",
        "weight_grams": 80,
        "calories_per_100g": 52,
        "protein_per_100g": 0.3
    },
    {
        "food_name": "苹果",
        "portion_name": "拳头大小（正常苹果，约150g）",
        "weight_grams": 150,
        "calories_per_100g": 52,
        "protein_per_100g": 0.3
    },
    {
        "food_name": "苹果",
        "portion_name": "拳头大小×1.5（大苹果，约225g）",
        "weight_grams": 225,
        "calories_per_100g": 52,
        "protein_per_100g": 0.3
    },

    # 香蕉
    {
        "food_name": "香蕉",
        "portion_name": "一根（小，约80g）",
        "weight_grams": 80,
        "calories_per_100g": 89,
        "protein_per_100g": 1.1
    },
    {
        "food_name": "香蕉",
        "portion_name": "一根（正常，约120g）",
        "weight_grams": 120,
        "calories_per_100g": 89,
        "protein_per_100g": 1.1
    },

    # 橙子
    {
        "food_name": "橙子",
        "portion_name": "拳头大小（约150g）",
        "weight_grams": 150,
        "calories_per_100g": 47,
        "protein_per_100g": 0.9
    },

    # 葡萄
    {
        "food_name": "葡萄",
        "portion_name": "一小串（约80g）",
        "weight_grams": 80,
        "calories_per_100g": 69,
        "protein_per_100g": 0.7
    },

    # ========== 蔬菜类 ==========
    # 生菜沙拉 - 双手一捧参考
    {
        "food_name": "生菜沙拉",
        "portion_name": "一手抓起的量（约30g）",
        "weight_grams": 30,
        "calories_per_100g": 20,
        "protein_per_100g": 1.5
    },
    {
        "food_name": "生菜沙拉",
        "portion_name": "双手一捧（约80g）",
        "weight_grams": 80,
        "calories_per_100g": 20,
        "protein_per_100g": 1.5
    },
    {
        "food_name": "生菜沙拉",
        "portion_name": "双手一捧×1.5（约120g）",
        "weight_grams": 120,
        "calories_per_100g": 20,
        "protein_per_100g": 1.5
    },

    # 青菜
    {
        "food_name": "青菜",
        "portion_name": "双手一捧（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 25,
        "protein_per_100g": 2
    },

    # 西兰花
    {
        "food_name": "西兰花",
        "portion_name": "双手一捧（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 34,
        "protein_per_100g": 2.8
    },

    # ========== 主食类 ==========
    # 米饭 - 碗参考
    {
        "food_name": "米饭",
        "portion_name": "一小碗（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 130,
        "protein_per_100g": 2.7
    },
    {
        "food_name": "米饭",
        "portion_name": "平时饭碗的一碗（约150g）",
        "weight_grams": 150,
        "calories_per_100g": 130,
        "protein_per_100g": 2.7
    },
    {
        "food_name": "米饭",
        "portion_name": "平时饭碗的一碗半（约225g）",
        "weight_grams": 225,
        "calories_per_100g": 130,
        "protein_per_100g": 2.7
    },

    # 面条
    {
        "food_name": "面条",
        "portion_name": "一小碗（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 140,
        "protein_per_100g": 4
    },

    # 意大利面
    {
        "food_name": "意大利面",
        "portion_name": "一小碗（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 131,
        "protein_per_100g": 5
    },

    # 全麦面包
    {
        "food_name": "全麦面包",
        "portion_name": "一片（约30g）",
        "weight_grams": 30,
        "calories_per_100g": 250,
        "protein_per_100g": 10
    },
    {
        "food_name": "全麦面包",
        "portion_name": "两片（约60g）",
        "weight_grams": 60,
        "calories_per_100g": 250,
        "protein_per_100g": 10
    },

    # ========== 蛋类 ==========
    # 鸡蛋
    {
        "food_name": "鸡蛋",
        "portion_name": "水煮蛋1个（约50g）",
        "weight_grams": 50,
        "calories_per_100g": 155,
        "protein_per_100g": 13
    },
    {
        "food_name": "鸡蛋",
        "portion_name": "煎蛋1个（约60g）",
        "weight_grams": 60,
        "calories_per_100g": 180,
        "protein_per_100g": 13
    },

    # ========== 乳制品类 ==========
    # 牛奶 - 杯参考
    {
        "food_name": "牛奶",
        "portion_name": "一小杯（约150ml）",
        "weight_grams": 150,
        "calories_per_100g": 54,
        "protein_per_100g": 3
    },
    {
        "food_name": "牛奶",
        "portion_name": "一杯（约250ml）",
        "weight_grams": 250,
        "calories_per_100g": 54,
        "protein_per_100g": 3
    },

    # 酸奶
    {
        "food_name": "酸奶",
        "portion_name": "小杯（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 60,
        "protein_per_100g": 4
    },
    {
        "food_name": "酸奶",
        "portion_name": "一杯（约150g）",
        "weight_grams": 150,
        "calories_per_100g": 60,
        "protein_per_100g": 4
    },

    # 奶酪
    {
        "food_name": "奶酪",
        "portion_name": "一小块（约20g）",
        "weight_grams": 20,
        "calories_per_100g": 402,
        "protein_per_100g": 25
    },

    # ========== 豆制品类 ==========
    # 豆腐
    {
        "food_name": "豆腐",
        "portion_name": "掌心大小（约100g）",
        "weight_grams": 100,
        "calories_per_100g": 76,
        "protein_per_100g": 8
    },

    # 豆浆
    {
        "food_name": "豆浆",
        "portion_name": "一杯（约250ml）",
        "weight_grams": 250,
        "calories_per_100g": 35,
        "protein_per_100g": 3
    },
]


def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")

    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("✓ 数据库表创建完成")

    # 创建会话
    db: Session = SessionLocal()

    try:
        # 清空现有数据（可选）
        existing_count = db.query(VisualPortion).count()
        if existing_count > 0:
            print(f"发现 {existing_count} 条现有记录")
            choice = input("是否清空现有数据？(y/n): ").lower()
            if choice == 'y':
                db.query(VisualPortion).delete()
                db.commit()
                print("✓ 现有数据已清空")

        # 插入食物份量数据
        inserted_count = 0
        for data in FOOD_PORTIONS_DATA:
            # 检查是否已存在
            existing = db.query(VisualPortion).filter(
                VisualPortion.food_name == data["food_name"],
                VisualPortion.portion_name == data["portion_name"]
            ).first()

            if not existing:
                portion = VisualPortion(**data)
                db.add(portion)
                inserted_count += 1

        db.commit()
        print(f"✓ 插入 {inserted_count} 条新记录")

        # 生成数据库状态报告
        generate_database_report(db)

    except Exception as e:
        db.rollback()
        print(f"✗ 初始化失败: {str(e)}")
        raise
    finally:
        db.close()


def generate_database_report(db: Session):
    """生成数据库状态报告"""
    print("\n" + "="*60)
    print("数据库状态报告")
    print("="*60)

    # 统计食物种类
    foods = db.query(VisualPortion.food_name).distinct().all()
    print(f"食物种类: {len(foods)}")

    # 按类别统计
    categories = {
        "肉类/禽类/鱼类": ["鸡胸肉", "牛肉", "牛排", "红烧肉", "鱼", "虾"],
        "水果": ["苹果", "香蕉", "橙子", "葡萄"],
        "蔬菜": ["生菜沙拉", "青菜", "西兰花"],
        "主食": ["米饭", "面条", "意大利面", "全麦面包"],
        "蛋类": ["鸡蛋"],
        "乳制品": ["牛奶", "酸奶", "奶酪"],
        "豆制品": ["豆腐", "豆浆"],
    }

    print("\n各类别份量选项统计:")
    for category, food_list in categories.items():
        total_portions = 0
        for food in food_list:
            count = db.query(VisualPortion).filter(
                VisualPortion.food_name == food
            ).count()
            total_portions += count

        if total_portions > 0:
            print(f"  {category}: {total_portions} 个份量选项")

    # 列出所有食物及其份量
    print("\n详细食物列表:")
    for food_name, in foods:
        portions = db.query(VisualPortion).filter(
            VisualPortion.food_name == food_name
        ).order_by(VisualPortion.weight_grams).all()

        print(f"\n  {food_name} ({len(portions)} 个份量选项):")
        for p in portions:
            calories = p.get_calories()
            protein = p.get_protein()
            print(f"    - {p.portion_name}: {calories:.0f}大卡, {protein:.1f}g蛋白质")

    print("\n" + "="*60)
    print("数据库初始化完成！")
    print("="*60)


if __name__ == "__main__":
    init_database()
