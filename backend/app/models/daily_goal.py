"""
每日目标模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base


class DailyGoal(Base):
    """每日目标 - 新目标覆盖旧目标"""
    __tablename__ = "daily_goals"

    id = Column(Integer, primary_key=True, index=True)
    gender = Column(String(10), nullable=False)  # "男" 或 "女"
    age = Column(Integer, nullable=False)
    height_cm = Column(Float, nullable=False)
    weight_kg = Column(Float, nullable=False)
    deficit_target = Column(Integer, nullable=False)  # 热量缺口：0/-300/-500/-800
    calorie_target = Column(Float, nullable=False)    # 计算得出的每日热量目标
    protein_target = Column(Float, nullable=False)    # 计算得出的每日蛋白质目标
    created_at = Column(DateTime, default=datetime.utcnow)

    def calculate_targets(self):
        """
        根据身体数据和热量缺口计算每日目标

        BMR 计算公式（Mifflin-St Jeor）：
        - 男性：BMR = 10 × 体重kg + 6.25 × 身高cm - 5 × 年龄 + 5
        - 女性：BMR = 10 × 体重kg + 6.25 × 身高cm - 5 × 年龄 - 161

        TDEE = BMR × 活动系数（假设久坐 1.2）
        每日目标 = TDEE + 热量缺口

        蛋白质目标 = 体重kg × 1.6g（减脂期推荐）
        """
        # 计算 BMR
        if self.gender == "男":
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age + 5
        else:
            bmr = 10 * self.weight_kg + 6.25 * self.height_cm - 5 * self.age - 161

        # TDEE（假设久坐，活动系数 1.2）
        tdee = bmr * 1.2

        # 每日热量目标
        self.calorie_target = tdee + self.deficit_target

        # 蛋白质目标（减脂期推荐 1.6g/kg）
        self.protein_target = self.weight_kg * 1.6

    @classmethod
    def get_latest_goal(cls, db):
        """获取最新的目标"""
        return db.query(cls).order_by(cls.created_at.desc()).first()

    def __repr__(self):
        return f"<DailyGoal({self.calorie_target:.0f}kcal, {self.protein_target:.0f}g protein)>"
