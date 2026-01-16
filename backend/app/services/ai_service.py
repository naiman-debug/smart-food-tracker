"""
AI 识别服务 - 集成智谱AI GLM-4.6V-Flash 图像识别
支持真实AI识别和模拟降级
支持单食物和多食物识别
"""
import os
import json
import random
import httpx
from typing import Dict, List, Optional, Tuple
from sqlalchemy.orm import Session
from ..models.visual_portion import VisualPortion
from pydantic import BaseModel


class GLMError(Exception):
    """GLM API 调用错误"""
    pass


class FoodRecognition(BaseModel):
    """食物识别结果"""
    food_name: str
    confidence: float = 1.0  # 识别置信度


class MultiFoodRecognition(BaseModel):
    """多食物识别结果"""
    foods: List[FoodRecognition]
    ai_used: bool


class AIService:
    """AI 食物识别服务"""

    # GLM API 配置
    GLM_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    GLM_MODEL = "glm-4.6v-flash"  # 免费视觉模型

    # 模拟AI识别结果 - 降级使用
    MOCK_RECOGNITION_RESULTS = [
        {"name": "鸡胸肉"},
        {"name": "红烧肉"},
        {"name": "米饭"},
        {"name": "苹果"},
        {"name": "生菜沙拉"},
        {"name": "鸡蛋"},
        {"name": "香蕉"},
        {"name": "牛奶"},
        {"name": "酸奶"},
        {"name": "全麦面包"},
    ]

    # 食物名称映射 - 将GLM识别结果映射到知识库标准名称（扩展版 - 覆盖100+食物）
    FOOD_NAME_MAPPING = {
        # ========== 肉类/禽类/鱼类 ==========
        "鸡胸肉": "鸡胸肉", "鸡肉": "鸡胸肉", "白切鸡": "鸡胸肉", "宫保鸡丁": "鸡胸肉",
        "口水鸡": "鸡胸肉", "辣子鸡": "鸡胸肉", "鸡柳": "鸡胸肉", "鸡排": "鸡胸肉",
        "鸡翅": "鸡翅", "鸡腿": "鸡腿",
        "牛肉": "牛肉", "牛排": "牛排", "红烧牛肉": "牛肉", "肥牛": "牛肉", "瘦牛肉": "牛肉",
        "猪肉": "猪肉", "五花肉": "五花肉", "梅花肉": "猪肉", "里脊肉": "猪肉",
        "红烧肉": "红烧肉", "排骨": "排骨", "猪排": "排骨", "糖醋排骨": "排骨",
        "鱼": "鱼", "清蒸鱼": "鱼", "红烧鱼": "鱼", "鲈鱼": "鱼", "草鱼": "鱼", "鲫鱼": "鱼",
        "虾": "虾", "白灼虾": "虾", "油焖大虾": "虾", "虾仁": "虾", "基围虾": "虾",
        "螃蟹": "螃蟹", "大闸蟹": "螃蟹", "梭子蟹": "螃蟹", "毛蟹": "螃蟹",
        "鸭肉": "鸭肉", "烤鸭": "鸭肉", "盐水鸭": "鸭肉", "酱鸭": "鸭肉",
        "羊肉": "羊肉", "羊肉串": "羊肉", "羊排": "羊肉", "红烧羊肉": "羊肉",
        "培根": "培根", "烟肉": "培根", "熏肉": "培根", "咸肉": "培根",
        "火腿": "火腿", "火腿肠": "火腿", "午餐肉": "火腿",
        "香肠": "香肠", "腊肠": "香肠", "广式腊肠": "香肠", "红肠": "香肠",
        "肉丸": "肉丸", "牛肉丸": "肉丸", "鱼丸": "肉丸", "虾丸": "肉丸",
        "火锅丸子": "火锅丸子", "撒尿牛丸": "火锅丸子", "贡丸": "火锅丸子", "鱼豆腐": "火锅丸子",

        # ========== 蔬菜类 ==========
        "生菜沙拉": "生菜沙拉", "沙拉": "生菜沙拉", "蔬菜沙拉": "生菜沙拉",
        "青菜": "青菜", "小白菜": "青菜", "油菜": "青菜", "绿叶菜": "青菜",
        "菠菜": "菠菜", "凉拌菠菜": "菠菜", "清炒菠菜": "菠菜",
        "西兰花": "西兰花", "西蓝花": "西兰花", "花椰菜": "西兰花",
        "白菜": "白菜", "大白菜": "白菜", "娃娃菜": "白菜", "圆白菜": "白菜",
        "胡萝卜": "胡萝卜", "红萝卜": "胡萝卜", "炒胡萝卜": "胡萝卜",
        "番茄": "番茄", "西红柿": "番茄", "番茄炒蛋": "番茄",
        "黄瓜": "黄瓜", "凉拌黄瓜": "黄瓜", "拍黄瓜": "黄瓜",
        "土豆": "土豆", "马铃薯": "土豆", "土豆丝": "土豆", "炸土豆": "土豆", "烤土豆": "土豆",
        "茄子": "茄子", "烤茄子": "茄子", "鱼香茄子": "茄子", "地三鲜": "茄子",
        "豆角": "豆角", "四季豆": "豆角", "长豆角": "豆角", "干煸豆角": "豆角",
        "莲藕": "莲藕", "藕片": "莲藕", "糖醋藕": "莲藕",
        "菌菇": "菌菇", "香菇": "菌菇", "平菇": "菌菇", "金针菇": "菌菇", "蘑菇": "菌菇",
        "海带": "海带", "凉拌海带": "海带", "海带丝": "海带",
        "豆芽": "豆芽", "绿豆芽": "豆芽", "黄豆芽": "豆芽",
        "冬瓜": "冬瓜", "冬瓜汤": "冬瓜",
        "南瓜": "南瓜", "蒸南瓜": "南瓜", "南瓜汤": "南瓜",

        # ========== 水果类 ==========
        "苹果": "苹果", "红富士": "苹果", "青苹果": "苹果",
        "香蕉": "香蕉",
        "橙子": "橙子", "橘子": "橙子", "砂糖橘": "橙子",
        "葡萄": "葡萄", "提子": "葡萄", "巨峰葡萄": "葡萄",
        "西瓜": "西瓜",
        "梨": "梨", "香梨": "梨", "雪梨": "梨",
        "桃子": "桃子", "水蜜桃": "桃子", "油桃": "桃子",
        "猕猴桃": "猕猴桃", "奇异果": "猕猴桃",
        "芒果": "芒果",
        "草莓": "草莓",
        "蓝莓": "蓝莓",
        "樱桃": "樱桃",

        # ========== 主食类 ==========
        "米饭": "米饭", "白米饭": "米饭", "蒸饭": "米饭", "粳米": "米饭",
        "面条": "面条", "拉面": "面条", "汤面": "面条", "炒面": "面条", "干面": "面条",
        "意大利面": "意大利面", "意面": "意大利面", "pasta": "意大利面", "肉酱面": "意大利面",
        "全麦面包": "全麦面包", "全麦吐司": "全麦面包", "黑麦面包": "全麦面包",
        "白面包": "白面包", "吐司": "白面包", "切片面包": "白面包", "三明治面包": "白面包",
        "馒头": "馒头", "蒸馒头": "馒头", "白馒头": "馒头", "花卷": "馒头",
        "包子": "包子", "肉包": "包子", "菜包": "包子", "豆沙包": "包子",
        "饺子": "饺子", "水饺": "饺子", "煎饺": "饺子", "蒸饺": "饺子",
        "馄饨": "馄饨", "云吞": "馄饨", "抄手": "馄饨",
        "煎饼": "煎饼", "煎饼果子": "煎饼", "鸡蛋饼": "煎饼",
        "油条": "油条",
        "粥": "粥", "白粥": "粥", "小米粥": "粥", "皮蛋瘦肉粥": "粥",
        "年糕": "年糕", "炒年糕": "年糕", "糖年糕": "年糕",
        "粽子": "粽子", "肉粽": "粽子", "蛋黄粽": "粽子", "豆沙粽": "粽子",
        "烧麦": "烧麦", "烧卖": "烧麦",
        "炒饭": "炒饭", "蛋炒饭": "炒饭", "扬州炒饭": "炒饭", "海鲜炒饭": "炒饭",
        "炒面": "炒面", "蛋炒面": "炒面", "肉丝炒面": "炒面",

        # ========== 蛋类 ==========
        "鸡蛋": "鸡蛋", "水煮蛋": "鸡蛋", "煎蛋": "鸡蛋", "炒蛋": "鸡蛋",
        "西红柿炒鸡蛋": "鸡蛋", "鸡蛋羹": "鸡蛋",
        "鸭蛋": "鸭蛋", "咸鸭蛋": "鸭蛋", "皮蛋": "鸭蛋",
        "鹌鹑蛋": "鹌鹑蛋", "卤蛋": "鹌鹑蛋", "虎皮蛋": "鹌鹑蛋",

        # ========== 乳制品类 ==========
        "牛奶": "牛奶", "纯牛奶": "牛奶", "鲜奶": "牛奶",
        "酸奶": "酸奶", "酸牛奶": "酸奶", "发酵乳": "酸奶",
        "奶酪": "奶酪", "芝士": "奶酪", "起司": "奶酪", "奶油芝士": "奶酪",
        "奶粉": "奶粉", "牛奶粉": "奶粉",
        "黄油": "黄油", "奶油": "黄油",

        # ========== 豆制品类 ==========
        "豆腐": "豆腐", "嫩豆腐": "豆腐", "老豆腐": "豆腐", "北豆腐": "豆腐",
        "豆浆": "豆浆", "豆奶": "豆浆", "生磨豆浆": "豆浆",
        "豆皮": "豆皮", "腐竹": "豆皮", "油皮": "豆皮",
        "腐竹": "腐竹", "干腐竹": "腐竹",

        # ========== 坚果零食类 ==========
        "花生": "花生", "炒花生": "花生", "煮花生": "花生",
        "核桃": "核桃", "胡桃": "核桃",
        "杏仁": "杏仁", "巴旦木": "杏仁",
        "瓜子": "瓜子", "葵花籽": "瓜子", "西瓜子": "瓜子",
        "薯片": "薯片", "potato chips": "薯片",
        "薯条": "薯条", "french fries": "薯条",
        "爆米花": "爆米花",
        "巧克力": "巧克力", "黑巧克力": "巧克力", "牛奶巧克力": "巧克力",

        # ========== 外卖常见菜品 ==========
        "宫保鸡丁": "宫保鸡丁", "花生鸡丁": "宫保鸡丁",
        "鱼香肉丝": "鱼香肉丝",
        "麻婆豆腐": "麻婆豆腐",
        "回锅肉": "回锅肉",
        "糖醋排骨": "糖醋排骨",
        "水煮鱼": "水煮鱼",
        "清炒时蔬": "清炒时蔬", "时蔬": "清炒时蔬",

        # ========== 早餐常见 ==========
        "玉米": "玉米", "煮玉米": "玉米", "烤玉米": "玉米",
        "红薯": "红薯", "番薯": "红薯", "烤红薯": "红薯",
    }

    @classmethod
    def get_api_key(cls) -> Optional[str]:
        """获取GLM API密钥"""
        return os.getenv("GLM_API_KEY")

    @classmethod
    def is_glm_enabled(cls) -> bool:
        """检查是否启用GLM"""
        api_key = cls.get_api_key()
        return api_key is not None and api_key.strip() != ""

    @classmethod
    def normalize_food_name(cls, raw_name: str) -> str:
        """
        标准化食物名称
        将GLM识别的食物名称映射到知识库标准名称
        """
        # 去除空格和特殊字符
        name = raw_name.strip().replace("，", "").replace("。", "")

        # 尝试精确匹配
        if name in cls.FOOD_NAME_MAPPING:
            return cls.FOOD_NAME_MAPPING[name]

        # 尝试模糊匹配（包含关系）
        for key, value in cls.FOOD_NAME_MAPPING.items():
            if key in name or name in key:
                return value

        # 无法映射，返回原始名称（可能导致404）
        return name

    @classmethod
    async def analyze_image_with_glm(cls, image_base64: str, multi_food: bool = False) -> List[str]:
        """
        使用GLM API分析食物图片

        Args:
            image_base64: base64编码的图片数据（不含data:image前缀）
            multi_food: 是否支持多食物识别

        Returns:
            识别出的食物名称列表

        Raises:
            GLMError: API调用失败时抛出
        """
        api_key = cls.get_api_key()
        if not api_key:
            raise GLMError("GLM_API_KEY 环境变量未设置")

        # 构建请求
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # 根据是否支持多食物选择不同的prompt（优化版 - 强调中式食物识别）
        if multi_food:
            prompt = """请识别这张图片中的中式食物，列出所有可见的食物。

【重要】这是中国食物记录应用，请优先识别中式常见食物：
- 肉类：鸡胸肉、牛肉、猪肉、排骨、鱼、虾、羊肉等
- 主食：米饭、面条、饺子、馒头、包子、粥等
- 蔬菜：青菜、白菜、西兰花、菠菜、番茄、黄瓜等
- 豆制品：豆腐、豆浆、豆皮等
- 蛋类：鸡蛋、鸭蛋等

识别要求：
1. 用逗号分隔多个食物名称，如：鸡胸肉,米饭,青菜
2. 优先使用食物基础名称（如"鸡胸肉"而非"宫保鸡丁"）
3. 不要回答烹饪方式、口感描述或装饰物
4. 如果只有一个食物，只返回一个名称
5. 最多返回3个主要食物"""
        else:
            prompt = """请识别这张图片中的中式食物，只回答食物的名称，不要添加任何其他描述。

【重要】这是中国食物记录应用，请优先识别中式常见食物：
- 肉类：鸡胸肉、牛肉、猪肉、排骨、鱼、虾、羊肉等
- 主食：米饭、面条、饺子、馒头、包子、粥等
- 蔬菜：青菜、白菜、西兰花、菠菜、番茄、黄瓜等
- 豆制品：豆腐、豆浆、豆皮等
- 蛋类：鸡蛋、鸭蛋等

识别要求：
1. 只返回最主要/主食/主菜的食物名称
2. 优先使用食物基础名称（如"鸡胸肉"而非"宫保鸡丁"）
3. 不要回答烹饪方式或口感描述
4. 如果有多个食物，只回答最主要的一个"""

        payload = {
            "model": cls.GLM_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_base64
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ],
            "temperature": 0.3,  # 降低温度以获得更一致的输出
            "top_p": 0.7,
            "max_tokens": 50
        }

        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    cls.GLM_API_URL,
                    headers=headers,
                    json=payload
                )

                # 处理响应
                if response.status_code == 200:
                    data = response.json()
                    if data.get("choices"):
                        content = data["choices"][0]["message"]["content"]
                        # 清理响应内容
                        content = content.strip().strip("。""，""、"".")

                        if multi_food:
                            # 多食物识别：解析逗号分隔的食物列表
                            food_names = [name.strip() for name in content.split(",")]
                            # 标准化每个食物名称
                            normalized_names = [cls.normalize_food_name(name) for name in food_names if name.strip()]
                            return normalized_names if normalized_names else [cls.normalize_food_name(content)]
                        else:
                            # 单食物识别：返回单个食物名称
                            food_name = content
                            return [food_name]
                    else:
                        raise GLMError("GLM API 返回格式异常")
                elif response.status_code == 401:
                    raise GLMError("GLM API密钥无效")
                elif response.status_code == 429:
                    raise GLMError("GLM API 请求频率超限")
                elif response.status_code >= 500:
                    raise GLMError(f"GLM API 服务错误: {response.status_code}")
                else:
                    error_detail = response.text
                    try:
                        error_json = response.json()
                        error_detail = error_json.get("error", {}).get("message", error_detail)
                    except:
                        pass
                    raise GLMError(f"GLM API 调用失败: {response.status_code} - {error_detail}")

        except httpx.TimeoutException:
            raise GLMError("GLM API 请求超时")
        except httpx.NetworkError as e:
            raise GLMError(f"GLM API 网络错误: {str(e)}")
        except json.JSONDecodeError:
            raise GLMError("GLM API 响应解析失败")

    @classmethod
    def mock_analyze_image(cls, image_base64: str) -> str:
        """
        模拟AI图片识别（降级方案）
        当GLM不可用时使用
        """
        result = random.choice(cls.MOCK_RECOGNITION_RESULTS)
        return result["name"]

    @classmethod
    def mock_analyze_multi_image(cls, image_base64: str, count: int = 1) -> List[str]:
        """
        模拟多食物AI图片识别（降级方案）
        """
        # 随机返回1-3个食物
        actual_count = min(count, len(cls.MOCK_RECOGNITION_RESULTS))
        results = random.sample(cls.MOCK_RECOGNITION_RESULTS, actual_count)
        return [r["name"] for r in results]

    @classmethod
    async def analyze_image(cls, image_base64: str) -> Tuple[str, bool]:
        """
        分析食物图片，返回识别结果（单食物）

        Args:
            image_base64: base64编码的图片数据

        Returns:
            (食物名称, 是否使用真实AI识别)
        """
        food_names, ai_used = await cls.analyze_image_multi(image_base64, multi_food=False)
        return food_names[0] if food_names else cls.mock_analyze_image(image_base64), ai_used

    @classmethod
    async def analyze_image_multi(cls, image_base64: str, multi_food: bool = True) -> Tuple[List[str], bool]:
        """
        分析食物图片，返回识别结果（支持多食物）

        Args:
            image_base64: base64编码的图片数据
            multi_food: 是否支持多食物识别

        Returns:
            (食物名称列表, 是否使用真实AI识别)
        """
        if cls.is_glm_enabled():
            try:
                raw_names = await cls.analyze_image_with_glm(image_base64, multi_food=multi_food)
                normalized_names = [cls.normalize_food_name(name) for name in raw_names]
                return normalized_names, True
            except GLMError as e:
                # GLM调用失败，降级到模拟识别
                print(f"GLM识别失败，降级到模拟识别: {str(e)}")
                count = 2 if multi_food else 1
                return cls.mock_analyze_multi_image(image_base64, count), False
        else:
            # GLM未配置，使用模拟识别
            print("GLM未配置，使用模拟识别")
            count = 2 if multi_food else 1
            return cls.mock_analyze_multi_image(image_base64, count), False

    @classmethod
    def get_portion_options_for_food(cls, db: Session, food_name: str) -> List[Dict]:
        """
        获取指定食物的视觉份量选项
        从 VisualPortion 表中查询该食物的所有份量选项

        Args:
            db: 数据库会话
            food_name: 食物名称

        Returns:
            份量选项列表，每个选项包含 id, portion_name, weight_grams, calories, protein
        """
        portions = db.query(VisualPortion).filter(
            VisualPortion.food_name == food_name
        ).all()

        if not portions:
            return []

        return [
            {
                "id": p.id,
                "food_name": p.food_name,
                "portion_name": p.portion_name,
                "weight_grams": p.weight_grams,
                "calories": p.get_calories(),
                "protein": p.get_protein()
            }
            for p in portions
        ]

    @classmethod
    def get_all_available_foods(cls, db: Session) -> List[str]:
        """
        获取知识库中所有可用的食物名称
        用于调试和验证
        """
        foods = db.query(VisualPortion.food_name).distinct().all()
        return [f[0] for f in foods]


# 便捷函数
async def analyze_food_image(image_base64: str) -> Tuple[str, bool]:
    """
    便捷函数：分析食物图片

    Returns:
        (食物名称, 是否使用真实AI)
    """
    return await AIService.analyze_image(image_base64)
