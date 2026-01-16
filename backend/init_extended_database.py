"""
扩展食物数据库初始化脚本
将 extended_food_database.py 中的105种食物导入数据库
"""
import sys
import os

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.models.database import Base, engine, get_db
from app.models.visual_portion import VisualPortion
from app.models.meal_record import MealRecord
from app.models.daily_goal import DailyGoal
from app.data.extended_food_database import EXTENDED_FOOD_DATABASE, FOOD_CATEGORIES


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


def print_success(text: str):
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str):
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_info(text: str):
    print(f"{Colors.YELLOW}○{Colors.RESET} {text}")


def create_tables():
    """创建所有数据库表"""
    print_header("创建数据库表")

    try:
        # 导入所有模型以确保它们被注册到 Base.metadata
        from app.models import (  # noqa: F401
            visual_portion, meal_record, daily_goal
        )

        # 创建所有表
        Base.metadata.create_all(bind=engine)
        print_success("数据库表创建成功")
        return True
    except Exception as e:
        print_error(f"创建数据库表失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def clear_existing_data(db: Session) -> int:
    """清除现有的食物数据"""
    try:
        count = db.query(VisualPortion).count()
        if count > 0:
            db.query(VisualPortion).delete()
            db.commit()
            print_info(f"已清除 {count} 条现有记录")
        return count
    except Exception as e:
        db.rollback()
        print_error(f"清除现有数据失败: {str(e)}")
        return 0


def import_food_database(db: Session) -> dict:
    """导入食物数据到数据库"""
    stats = {
        "total_foods": len(EXTENDED_FOOD_DATABASE),
        "imported_foods": 0,
        "imported_portions": 0,
        "skipped_foods": 0,
        "category_stats": {},
        "errors": []
    }

    print_header("开始导入食物数据")

    for food_name, food_data in EXTENDED_FOOD_DATABASE.items():
        category = food_data["category"]
        calories_per_100g = food_data["calories_per_100g"]
        protein_per_100g = food_data["protein_per_100g"]
        portions = food_data["portions"]

        # 统计分类
        if category not in stats["category_stats"]:
            stats["category_stats"][category] = {"foods": 0, "portions": 0}
        stats["category_stats"][category]["foods"] += 1

        try:
            # 为每个份量选项创建记录
            for i, portion in enumerate(portions):
                visual_portion = VisualPortion(
                    food_name=food_name,
                    portion_name=portion["name"],
                    weight_grams=portion["weight"],
                    calories_per_100g=calories_per_100g,
                    protein_per_100g=protein_per_100g
                )
                db.add(visual_portion)
                stats["imported_portions"] += 1
                stats["category_stats"][category]["portions"] += 1

            stats["imported_foods"] += 1
            print_success(f"{food_name} ({category}) - {len(portions)}个份量选项")

        except Exception as e:
            db.rollback()
            error_msg = f"{food_name}: {str(e)}"
            stats["errors"].append(error_msg)
            print_error(error_msg)
            stats["skipped_foods"] += 1

    # 提交所有更改
    try:
        db.commit()
        print_success("\n所有数据导入成功")
    except Exception as e:
        db.rollback()
        print_error(f"\n提交数据失败: {str(e)}")
        stats["errors"].append(f"Commit failed: {str(e)}")

    return stats


def verify_imported_data(db: Session, stats: dict) -> bool:
    """验证导入的数据"""
    print_header("验证导入的数据")

    # 验证总记录数
    total_portions = db.query(VisualPortion).count()
    expected_portions = stats["imported_portions"]

    if total_portions != expected_portions:
        print_error(f"份量记录数不匹配: 预期 {expected_portions}, 实际 {total_portions}")
        return False

    print_success(f"份量记录数验证通过: {total_portions} 条")

    # 验证唯一食物数
    from sqlalchemy import func
    unique_foods = db.query(
        func.count(func.distinct(VisualPortion.food_name))
    ).scalar()

    if unique_foods != stats["imported_foods"]:
        print_error(f"食物数量不匹配: 预期 {stats['imported_foods']}, 实际 {unique_foods}")
        return False

    print_success(f"食物数量验证通过: {unique_foods} 种")

    # 验证每个食物的份量选项
    print_header("验证份量选项PRD符合性")

    prd_compliance = {
        "掌心大小": ["肉类", "鱼类"],
        "信用卡厚度": ["肉类"],
        "网球大小": ["水果"],
        "拳头大小": ["水果", "土豆"],
        "双手一捧": ["蔬菜"],
        "一小碗": ["主食", "粥"],
        "水煮蛋": ["蛋类"],
        "一杯": ["乳制品", "豆浆"]
    }

    for food_name, food_data in EXTENDED_FOOD_DATABASE.items():
        portions = db.query(VisualPortion).filter(
            VisualPortion.food_name == food_name
        ).all()

        if not portions:
            print_error(f"{food_name}: 无份量数据")
            continue

        # 检查份量描述符合PRD
        for p in portions:
            portion_name = p.portion_name
            food_category = food_data["category"]

            # 验证份量描述包含PRD关键词
            has_prd_keyword = False
            for keyword, expected_categories in prd_compliance.items():
                if keyword in portion_name:
                    has_prd_keyword = True
                    break

            if not has_prd_keyword and food_category in ["meat", "fruit", "vegetable", "staple"]:
                print_info(f"{food_name}: {portion_name}")

    print_success("PRD符合性验证完成")

    return True


def print_statistics(stats: dict):
    """打印统计信息"""
    print_header("数据统计")

    print(f"食物种类: {Colors.GREEN}{stats['imported_foods']}{Colors.RESET} / {stats['total_foods']}")
    print(f"份量选项: {Colors.GREEN}{stats['imported_portions']}{Colors.RESET} 条")
    print(f"跳过食物: {Colors.YELLOW if stats['skipped_foods'] > 0 else ''}{stats['skipped_foods']}{Colors.RESET}")

    print(f"\n{Colors.BOLD}分类统计:{Colors.RESET}")
    for category_key, category_info in FOOD_CATEGORIES.items():
        if category_key in stats["category_stats"]:
            cat_stats = stats["category_stats"][category_key]
            print(f"  {category_info['icon']} {category_info['name']}: "
                  f"{Colors.GREEN}{cat_stats['foods']}种{Colors.RESET}, "
                  f"{cat_stats['portions']}个份量选项")

    if stats["errors"]:
        print(f"\n{Colors.RED}错误列表:{Colors.RESET}")
        for error in stats["errors"][:10]:  # 只显示前10个错误
            print(f"  {Colors.RED}✗{Colors.RESET} {error}")
        if len(stats["errors"]) > 10:
            print(f"  ... 还有 {len(stats['errors']) - 10} 个错误")


def main():
    """主函数"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}")
    print("╔════════════════════════════════════════╗")
    print("║   扩展食物数据库初始化脚本 (105种食物)   ║")
    print("╚════════════════════════════════════════╝")
    print(f"{Colors.RESET}")

    # 获取数据库会话
    db: Session = next(get_db())

    try:
        # Step 1: 创建数据库表（如果不存在）
        if not create_tables():
            print_error("数据库表创建失败，终止初始化")
            return 1

        # Step 2: 清除现有数据（可选，根据需要注释掉）
        print_header("清除现有数据")
        clear_existing_data(db)

        # 导入食物数据
        stats = import_food_database(db)

        # 验证导入的数据
        if stats["imported_foods"] > 0:
            verify_imported_data(db, stats)

        # 打印统计信息
        print_statistics(stats)

        # 最终状态
        print_header("初始化完成")

        if stats["errors"]:
            print(f"{Colors.YELLOW}注意: {len(stats['errors'])} 个错误发生，请检查日志{Colors.RESET}")
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}✓ 数据库初始化成功完成！{Colors.RESET}")
            print(f"\n{Colors.BOLD}下一步:{Colors.RESET}")
            print(f"  1. 配置 .env 文件中的 GLM_API_KEY")
            print(f"  2. 启动后端服务: uvicorn app.main:app --reload")
            print(f"  3. 启动前端服务: cd frontend && npm run dev")

    except Exception as e:
        print_error(f"\n初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        db.close()

    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
