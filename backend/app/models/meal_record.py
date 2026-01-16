"""
饮食记录模型 - 唯一数据源
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class MealRecord(Base):
    """饮食记录 - 唯一数据源"""
    __tablename__ = "meal_records"

    id = Column(Integer, primary_key=True, index=True)
    image_url = Column(String(500), nullable=False)
    food_name = Column(String(100), nullable=False)  # AI 识别的食物名称
    visual_portion_id = Column(Integer, ForeignKey("visual_portions.id"), nullable=False)
    calories = Column(Float, nullable=False)  # 从 VisualPortion 计算
    protein = Column(Float, nullable=False)   # 从 VisualPortion 计算
    record_date = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    visual_portion = relationship("VisualPortion", back_populates="meal_records")

    def __repr__(self):
        return f"<MealRecord({self.food_name}, {self.calories}kcal, {self.record_date})>"
