"""
API 路由包
"""
from .meal import router as meal_router
from .system import router as system_router

__all__ = ['meal_router', 'system_router']
