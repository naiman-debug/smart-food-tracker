"""
视觉份量知识库模型 - 每条记录 = 某种食物 + 某种视觉份量的完整营养定义
"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from .database import Base


class VisualPortion(Base):
    """视觉份量知识库"""
    __tablename__ = "visual_portions"

    id = Column(Integer, primary_key=True, index=True)
    food_name = Column(String(100), nullable=False, index=True)
    portion_name = Column(String(100), nullable=False)
    weight_grams = Column(Float, nullable=False)
    calories_per_100g = Column(Float, nullable=False)
    protein_per_100g = Column(Float, nullable=False)

    # 关系
    meal_records = relationship("MealRecord", back_populates="visual_portion")

    def get_calories(self) -> float:
        """计算该份量的热量"""
        return (self.weight_grams / 100) * self.calories_per_100g

    def get_protein(self) -> float:
        """计算该份量的蛋白质"""
        return (self.weight_grams / 100) * self.protein_per_100g

    def __repr__(self):
        return f"<VisualPortion({self.food_name} - {self.portion_name}, {self.weight_grams}g)>"
