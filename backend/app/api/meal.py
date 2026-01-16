"""
饮食记录核心 API
集成智谱AI GLM-4.6V-Flash 图像识别
支持单食物和多食物识别
支持AI识别失败后的食物分类选择备选流程
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List, Dict
from datetime import datetime, date, timedelta
import logging
import os

from ..models.database import get_db
from ..models.visual_portion import VisualPortion
from ..models.meal_record import MealRecord
from ..models.daily_goal import DailyGoal
from ..services.ai_service import AIService, GLMError
from ..services.portion_service import PortionService
from ..data.extended_food_database import EXTENDED_FOOD_DATABASE, FOOD_CATEGORIES
from pydantic import BaseModel


# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 环境变量：控制错误信息详细程度
# development: 显示详细错误信息（包括available_foods等）
# production: 显示简化的用户友好提示
ENV_MODE = os.getenv("ENV_MODE", "production")


router = APIRouter(prefix="/api", tags=["meal"])


# ============ 请求/响应模型 ============

class AnalyzeImageRequest(BaseModel):
    image_base64: str
    multi_food: bool = False  # 是否支持多食物识别


class FoodRecognitionItem(BaseModel):
    """单个食物识别结果"""
    food_name: str
    portion_options: list[PortionOption] = []


class AnalyzeImageResponse(BaseModel):
    """单食物识别响应"""
    food_name: str
    portion_options: list[PortionOption]
    ai_used: bool = False


class MultiFoodAnalyzeResponse(BaseModel):
    """多食物识别响应"""
    foods: list[FoodRecognitionItem]
    ai_used: bool = False


class PortionOption(BaseModel):
    id: int
    food_name: str
    portion_name: str
    weight_grams: float
    calories: float
    protein: float

    class Config:
        from_attributes = True


class CreateRecordRequest(BaseModel):
    image_url: str
    food_name: str
    visual_portion_id: int


class MealRecordResponse(BaseModel):
    id: int
    image_url: str
    food_name: str
    visual_portion_id: int
    calories: float
    protein: float
    record_date: datetime

    class Config:
        from_attributes = True


class DailyBalanceResponse(BaseModel):
    remaining_calories: float
    remaining_protein: float
    consumed_calories: float
    consumed_protein: float
    target_calories: float
    target_protein: float
    meals_count: int
    suggestions: list = []  # 智能建议列表


class SuggestionItem(BaseModel):
    id: int
    food_name: str
    portion_name: str
    calories: float
    protein: float
    reason: str  # 推荐理由


class ProgressResponse(BaseModel):
    total_calorie_deficit: float
    estimated_fat_lost: float
    days_tracked: int
    data_points: list
    encouragement: str


class SetGoalRequest(BaseModel):
    gender: str
    age: int
    height_cm: float
    weight_kg: float
    deficit_target: int


class GoalResponse(BaseModel):
    id: int
    gender: str
    age: int
    height_cm: float
    weight_kg: float
    deficit_target: int
    calorie_target: float
    protein_target: float

    class Config:
        from_attributes = True


# ============ 新增：食物分类相关数据模型 ============

class CategoryInfo(BaseModel):
    """食物分类信息"""
    key: str
    name: str
    icon: str
    description: str


class FoodItemInfo(BaseModel):
    """食物项信息"""
    name: str
    category: str
    aliases: List[str]
    calories_per_100g: float
    protein_per_100g: float
    portion_count: int


class FoodCategoryListResponse(BaseModel):
    """食物分类列表响应"""
    categories: List[CategoryInfo]


class FoodsByCategoryResponse(BaseModel):
    """按分类获取食物列表响应"""
    category: CategoryInfo
    foods: List[FoodItemInfo]


# ============ API 端点 ============

@router.get("/food-categories", response_model=FoodCategoryListResponse)
async def get_food_categories():
    """
    获取所有食物分类
    用于AI识别失败后的手动选择界面
    """
    categories = [
        CategoryInfo(
            key=key,
            name=info["name"],
            icon=info["icon"],
            description=info["description"]
        )
        for key, info in FOOD_CATEGORIES.items()
    ]

    return FoodCategoryListResponse(categories=categories)


@router.get("/foods-by-category/{category_key}", response_model=FoodsByCategoryResponse)
async def get_foods_by_category(category_key: str, db: Session = Depends(get_db)):
    """
    获取指定分类下的所有食物
    用于AI识别失败后的手动选择界面
    """
    # 验证分类是否存在
    if category_key not in FOOD_CATEGORIES:
        raise HTTPException(status_code=404, detail=f"分类「{category_key}」不存在")

    category_info = FOOD_CATEGORIES[category_key]

    # 获取该分类下的所有食物
    foods = []
    for food_name, food_data in EXTENDED_FOOD_DATABASE.items():
        if food_data["category"] == category_key:
            # 检查数据库中是否有份量数据
            portions = db.query(VisualPortion).filter(
                VisualPortion.food_name == food_name
            ).all()

            foods.append(FoodItemInfo(
                name=food_name,
                category=category_key,
                aliases=food_data["aliases"],
                calories_per_100g=food_data["calories_per_100g"],
                protein_per_100g=food_data["protein_per_100g"],
                portion_count=len(portions) if portions else 0
            ))

    # 按热量排序
    foods.sort(key=lambda f: f.calories_per_100g)

    return FoodsByCategoryResponse(
        category=CategoryInfo(
            key=category_key,
            name=category_info["name"],
            icon=category_info["icon"],
            description=category_info["description"]
        ),
        foods=foods
    )


@router.get("/food-search", response_model=List[FoodItemInfo])
async def search_foods(q: str, db: Session = Depends(get_db)):
    """
    搜索食物
    支持按名称或别名模糊搜索
    """
    if not q or len(q) < 1:
        return []

    q_lower = q.lower()
    results = []

    for food_name, food_data in EXTENDED_FOOD_DATABASE.items():
        # 检查名称是否匹配
        if q_lower in food_name.lower():
            portions = db.query(VisualPortion).filter(
                VisualPortion.food_name == food_name
            ).all()

            results.append(FoodItemInfo(
                name=food_name,
                category=food_data["category"],
                aliases=food_data["aliases"],
                calories_per_100g=food_data["calories_per_100g"],
                protein_per_100g=food_data["protein_per_100g"],
                portion_count=len(portions) if portions else 0
            ))
            continue

        # 检查别名是否匹配
        for alias in food_data["aliases"]:
            if q_lower in alias.lower():
                portions = db.query(VisualPortion).filter(
                    VisualPortion.food_name == food_name
                ).all()

                results.append(FoodItemInfo(
                    name=food_name,
                    category=food_data["category"],
                    aliases=food_data["aliases"],
                    calories_per_100g=food_data["calories_per_100g"],
                    protein_per_100g=food_data["protein_per_100g"],
                    portion_count=len(portions) if portions else 0
                ))
                break

    # 限制返回数量
    return results[:20]


@router.get("/portions/{food_name}", response_model=AnalyzeImageResponse)
async def get_portions_by_food_name(food_name: str, db: Session = Depends(get_db)):
    """
    根据食物名称直接获取份量选项（无需AI识别）
    用于用户手动选择食物后的备选流程
    """
    # 查询该食物的份量选项
    portion_options_data = PortionService.get_portion_options_for_food(db, food_name)

    if not portion_options_data:
        raise HTTPException(
            status_code=404,
            detail={
                "message": f"知识库中暂无「{food_name}」的数据",
                "code": "FOOD_NOT_FOUND"
            }
        )

    # 构建响应
    portion_options = [
        PortionOption(**option) for option in portion_options_data
    ]

    return AnalyzeImageResponse(
        food_name=food_name,
        portion_options=portion_options,
        ai_used=False
    )


@router.post("/analyze", response_model=AnalyzeImageResponse)
async def analyze_image(request: AnalyzeImageRequest, db: Session = Depends(get_db)):
    """
    分析食物图片（单食物）

    1. 使用 GLM-4.6V-Flash 识别食物名称
    2. 将识别结果映射到知识库标准名称
    3. 查询 VisualPortion 获取该食物的份量选项
    4. 返回份量选项（含计算好的热量和蛋白质）

    降级机制：
    - 如果 GLM_API_KEY 未配置，自动降级到模拟识别
    - 如果 GLM 调用失败（网络错误、限流等），自动降级到模拟识别
    """
    # AI 识别
    try:
        food_names, ai_used = await AIService.analyze_image_multi(request.image_base64, multi_food=False)
        food_name = food_names[0] if food_names else AIService.mock_analyze_image(request.image_base64)
        logger.info(f"AI识别结果: {food_name} (使用真实AI: {ai_used})")
    except Exception as e:
        logger.error(f"AI识别异常: {str(e)}")
        # 完全降级到模拟识别
        food_name = AIService.mock_analyze_image(request.image_base64)
        ai_used = False

    # 查询该食物的份量选项
    portions = db.query(VisualPortion).filter(
        VisualPortion.food_name == food_name
    ).all()

    if not portions:
        # 根据环境变量控制错误信息详细程度
        logger.warning(f"知识库中暂无「{food_name}」的数据")
        error_detail = _build_error_detail(food_name, ai_used, db)
        raise HTTPException(
            status_code=400 if ENV_MODE == "production" else 404,
            detail=error_detail
        )

    # 使用 PortionService 获取按PRD排序的份量选项
    portion_options_data = PortionService.get_portion_options_for_food(db, food_name)

    if not portion_options_data:
        # 如果排序后没有结果（不应该发生），返回原始错误
        logger.warning(f"份量选项为空: {food_name}")
        error_detail = _build_error_detail(food_name, ai_used, db)
        raise HTTPException(
            status_code=400 if ENV_MODE == "production" else 404,
            detail=error_detail
        )

    # 构建响应
    portion_options = [
        PortionOption(**option) for option in portion_options_data
    ]

    return AnalyzeImageResponse(
        food_name=food_name,
        portion_options=portion_options,
        ai_used=ai_used
    )


@router.post("/analyze-multi", response_model=MultiFoodAnalyzeResponse)
async def analyze_multi_food(request: AnalyzeImageRequest, db: Session = Depends(get_db)):
    """
    分析食物图片（支持多食物识别）

    返回图片中识别出的所有食物及其份量选项
    用户可以选择性地添加到一餐记录中
    """
    # AI 识别（多食物模式）
    try:
        food_names, ai_used = await AIService.analyze_image_multi(request.image_base64, multi_food=True)
        logger.info(f"多食物AI识别结果: {food_names} (使用真实AI: {ai_used})")
    except Exception as e:
        logger.error(f"多食物AI识别异常: {str(e)}")
        # 降级到模拟识别（返回1-2个随机食物）
        food_names = AIService.mock_analyze_multi_image(request.image_base64, count=2)
        ai_used = False

    # 为每个识别的食物获取份量选项
    food_items = []
    for food_name in food_names:
        portion_options_data = PortionService.get_portion_options_for_food(db, food_name)

        if portion_options_data:
            portion_options = [PortionOption(**option) for option in portion_options_data]
            food_items.append(FoodRecognitionItem(
                food_name=food_name,
                portion_options=portion_options
            ))

    # 如果没有找到任何有效食物
    if not food_items:
        logger.warning(f"多食物识别未找到有效食物: {food_names}")
        error_detail = _build_error_detail(food_names[0] if food_names else "未知食物", ai_used, db)
        raise HTTPException(
            status_code=400 if ENV_MODE == "production" else 404,
            detail=error_detail
        )

    return MultiFoodAnalyzeResponse(
        foods=food_items,
        ai_used=ai_used
    )


def _build_error_detail(food_name: str, ai_used: bool, db: Session) -> dict:
    """
    根据环境变量构建不同详细程度的错误信息

    生产环境: 简化的用户友好提示
    开发环境: 包含调试信息
    """
    if ENV_MODE == "production":
        return {
            "message": "识别有点困难，请选择食物类型",
            "code": "RECOGNITION_FAILED"
        }
    else:
        # 开发环境：返回详细错误信息
        available_foods = AIService.get_all_available_foods(db)
        return {
            "message": f"知识库中暂无「{food_name}」的数据",
            "recognized_food": food_name,
            "ai_used": ai_used,
            "available_foods": available_foods[:10],
            "code": "FOOD_NOT_FOUND"
        }


@router.post("/records", response_model=MealRecordResponse)
async def create_record(request: CreateRecordRequest, db: Session = Depends(get_db)):
    """
    创建饮食记录
    用户选择份量后调用此接口完成记录
    """
    # 查询 VisualPortion
    portion = db.query(VisualPortion).filter(
        VisualPortion.id == request.visual_portion_id
    ).first()

    if not portion:
        raise HTTPException(status_code=404, detail="份量选项不存在")

    # 创建记录（营养数据从 VisualPortion 计算）
    record = MealRecord(
        image_url=request.image_url,
        food_name=request.food_name,
        visual_portion_id=request.visual_portion_id,
        calories=portion.get_calories(),
        protein=portion.get_protein(),
        record_date=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    logger.info(f"创建记录: {request.food_name}, {portion.get_calories()}大卡")
    return record


@router.get("/balance", response_model=DailyBalanceResponse)
async def get_daily_balance(db: Session = Depends(get_db)):
    """
    获取今日余额
    返回今日剩余的热量和蛋白质额度，以及智能推荐食物
    """
    # 获取目标
    goal = DailyGoal.get_latest_goal(db)
    if goal:
        target_calories = goal.calorie_target
        target_protein = goal.protein_target
    else:
        target_calories = 2000  # 默认值
        target_protein = 120

    # 计算今日已摄入
    today = date.today()
    start_of_day = datetime.combine(today, datetime.min.time())
    end_of_day = datetime.combine(today, datetime.max.time())

    result = db.query(
        func.sum(MealRecord.calories).label("total_calories"),
        func.sum(MealRecord.protein).label("total_protein"),
        func.count(MealRecord.id).label("meals_count")
    ).filter(
        MealRecord.record_date >= start_of_day,
        MealRecord.record_date <= end_of_day
    ).first()

    consumed_calories = result.total_calories or 0
    consumed_protein = result.total_protein or 0
    meals_count = result.meals_count or 0

    remaining_calories = max(0, target_calories - consumed_calories)
    remaining_protein = max(0, target_protein - consumed_protein)

    # 生成智能建议
    suggestions = _generate_suggestions(db, remaining_calories, remaining_protein)

    return DailyBalanceResponse(
        remaining_calories=remaining_calories,
        remaining_protein=remaining_protein,
        consumed_calories=consumed_calories,
        consumed_protein=consumed_protein,
        target_calories=target_calories,
        target_protein=target_protein,
        meals_count=meals_count,
        suggestions=suggestions
    )


@router.get("/progress", response_model=ProgressResponse)
async def get_progress(
    range: Optional[str] = "all",
    db: Session = Depends(get_db)
):
    """
    获取进度统计
    range: week(本周), month(本月), all(全部)
    """
    # 获取目标
    goal = DailyGoal.get_latest_goal(db)
    if goal:
        target_calories = goal.calorie_target
    else:
        target_calories = 2000

    # 确定日期范围
    end_date = date.today()
    if range == "week":
        start_date = end_date - timedelta(days=7)
    elif range == "month":
        start_date = end_date - timedelta(days=30)
    else:  # all
        start_date = date.min

    # 查询记录
    records = db.query(
        func.date(MealRecord.record_date).label("date"),
        func.sum(MealRecord.calories).label("calories")
    ).filter(
        MealRecord.record_date >= datetime.combine(start_date, datetime.min.time()),
        MealRecord.record_date <= datetime.combine(end_date, datetime.max.time())
    ).group_by(
        func.date(MealRecord.record_date)
    ).all()

    # 计算每日缺口和累计
    total_deficit = 0
    data_points = []

    for record in records:
        daily_intake = record.calories or 0
        daily_deficit = target_calories - daily_intake
        total_deficit += daily_deficit

        data_points.append({
            "date": record.date.isoformat(),
            "calorie_deficit": round(daily_deficit, 2),
            "consumed_calories": round(daily_intake, 2)
        })

    # 估算减脂重量（7700kcal ≈ 1kg 脂肪）
    estimated_fat_lost = total_deficit / 7700

    return ProgressResponse(
        total_calorie_deficit=round(total_deficit, 2),
        estimated_fat_lost=round(estimated_fat_lost, 3),
        days_tracked=len(records),
        data_points=data_points,
        encouragement=_generate_encouragement(total_deficit)
    )


@router.post("/goals", response_model=GoalResponse)
async def set_goal(request: SetGoalRequest, db: Session = Depends(get_db)):
    """
    设置每日目标
    新目标会覆盖旧目标
    """
    # 验证 deficit_target
    if request.deficit_target not in [0, -300, -500, -800]:
        raise HTTPException(
            status_code=400,
            detail="deficit_target 必须是 0, -300, -500 或 -800"
        )

    # 验证 gender
    if request.gender not in ["男", "女"]:
        raise HTTPException(
            status_code=400,
            detail="gender 必须是 '男' 或 '女'"
        )

    goal = DailyGoal(
        gender=request.gender,
        age=request.age,
        height_cm=request.height_cm,
        weight_kg=request.weight_kg,
        deficit_target=request.deficit_target
    )
    goal.calculate_targets()

    db.add(goal)
    db.commit()
    db.refresh(goal)

    logger.info(f"设置目标: {goal.calorie_target}大卡, {goal.protein_target}g蛋白质")
    return goal


@router.get("/goals", response_model=Optional[GoalResponse])
async def get_current_goal(db: Session = Depends(get_db)):
    """获取当前目标"""
    return DailyGoal.get_latest_goal(db)


# ============ 辅助函数 ============

def _generate_suggestions(db: Session, remaining_calories: float, remaining_protein: float) -> list:
    """
    根据剩余额度生成智能推荐食物

    推荐逻辑：
    - 剩余 > 200kcal: 推荐水煮蛋、小杯酸奶等小份食物
    - 剩余 > 150kcal: 推荐掌心鸡胸肉等中等份量食物
    - 剩余 > 100kcal: 推荐蔬菜沙拉等低热量食物
    """
    suggestions = []

    # 定义推荐规则：(最小热量, 食物名称, 份量名称, 推荐理由)
    recommendation_rules = [
        # 小份加餐 (<100 kcal)
        (0, "鸡蛋", "水煮蛋1个（约50g）", "快速补充蛋白质"),
        (0, "酸奶", "小杯酸奶（约100g）", "益生菌助消化"),

        # 中等份量 (100-200 kcal)
        (100, "鸡胸肉", "掌心大小（正常厚度，约120g）", "优质蛋白"),
        (100, "苹果", "拳头大小（正常，约150g）", "富含维生素"),
        (100, "牛奶", "一杯（约250ml）", "补钙好选择"),

        # 较大份量 (>200 kcal)
        (200, "鸡胸肉", "掌心大小×1.5（厚切，约180g）", "高蛋白饱腹"),
        (200, "米饭", "一小碗（约150g）", "主食补充"),
        (200, "全麦面包", "一片（约30g）", "膳食纤维"),
    ]

    for min_calories, food_name, portion_desc, reason in recommendation_rules:
        if remaining_calories >= min_calories:
            # 查询数据库中该食物的最小份量选项
            portion = db.query(VisualPortion).filter(
                VisualPortion.food_name == food_name
            ).order_by(VisualPortion.calories_per_100g.asc()).first()

            if portion:
                calories = portion.get_calories()
                # 确保推荐的食物热量不超过剩余额度
                if calories <= remaining_calories:
                    suggestions.append({
                        "id": portion.id,
                        "food_name": food_name,
                        "portion_name": portion.portion_name,
                        "calories": round(calories, 1),
                        "protein": round(portion.get_protein(), 1),
                        "reason": reason
                    })

                    # 最多返回5个建议
                    if len(suggestions) >= 5:
                        break

    return suggestions


def _generate_encouragement(deficit: float) -> str:
    """根据进度生成鼓励语"""
    if deficit > 0:
        return "热量盈余，注意控制摄入！"
    elif deficit > -1000:
        return "好的开始，继续保持！"
    elif deficit > -3500:
        return "稳步前行，保持节奏！"
    elif deficit > -7700:
        return "非常棒！已经减掉约1kg脂肪！"
    else:
        return "太厉害了！你的坚持正在带来改变！"


# ============ 快速记录接口 ============

class QuickRecordRequest(BaseModel):
    visual_portion_id: int  # 直接使用份量ID快速记录


@router.post("/quick-record", response_model=MealRecordResponse)
async def create_quick_record(request: QuickRecordRequest, db: Session = Depends(get_db)):
    """
    快速记录 - 无需拍照
    用于智能建议的快捷记录功能
    """
    # 查询 VisualPortion
    portion = db.query(VisualPortion).filter(
        VisualPortion.id == request.visual_portion_id
    ).first()

    if not portion:
        raise HTTPException(status_code=404, detail="份量选项不存在")

    # 创建记录（无图片URL）
    record = MealRecord(
        image_url="",  # 快速记录无图片
        food_name=portion.food_name,
        visual_portion_id=request.visual_portion_id,
        calories=portion.get_calories(),
        protein=portion.get_protein(),
        record_date=datetime.utcnow()
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    logger.info(f"快速记录: {portion.food_name}, {portion.get_calories()}大卡")
    return record
