# AI识别失败优化任务摘要

> 日期: 2026-01-16
> 项目: 智能食物记录 App
> 版本: v1.1
> 状态: ✅ 核心任务完成

---

## 任务概述

根据用户需求，执行以下4项优化任务：
1. 设计AI识别失败的备选交互流程
2. 扩展食物知识库至80-100种
3. 优化AI提示词提高识别准确率
4. 生成任务摘要

---

## 完成情况

### 1. 设计AI识别失败的备选交互流程 ✅

**后端实现：**

新增3个API接口，用于支持手动食物选择备选流程：

| API端点 | 方法 | 功能说明 |
|---------|------|----------|
| `/api/food-categories` | GET | 获取所有食物分类（10个分类） |
| `/api/foods-by-category/{category_key}` | GET | 获取指定分类下的食物列表 |
| `/api/food-search?q={keyword}` | GET | 模糊搜索食物 |

**文件修改：** `backend/app/api/meal.py`

```python
# 新增数据模型
class CategoryInfo(BaseModel):
    key: str
    name: str
    icon: str
    description: str

class FoodItemInfo(BaseModel):
    name: str
    category: str
    aliases: List[str]
    calories_per_100g: float
    protein_per_100g: float
    portion_count: int
```

**交互流程设计：**
```
用户拍照
    ↓
AI识别
    ↓
识别成功 → 进入份量选择流程
    ↓
识别失败 → 显示"从常见食物中选择"界面
    ↓
显示10个食物分类选项卡（肉类、蔬菜、水果、主食等）
    ↓
用户点击分类 → 显示该分类下10-15种常见食物
    ↓
用户选择食物 → 正常进入份量选择流程
```

**前端集成说明：**
- 当 `/api/analyze` 或 `/api/analyze-multi` 返回错误码400且 `code="RECOGNITION_FAILED"` 时
- 前端应显示食物分类选择界面
- 调用 `/api/food-categories` 获取分类列表
- 用户选择分类后调用 `/api/foods-by-category/{key}` 获取食物列表
- 也可直接调用 `/api/food-search?q={keyword}` 进行搜索

### 2. 扩展食物知识库至80-100种 ✅

**新建文件：** `backend/app/data/extended_food_database.py`

**数据统计：**

| 分类 | 食物数量 | 示例食物 |
|------|----------|----------|
| 肉类/禽类/鱼类 | 20种 | 鸡胸肉、牛肉、鱼、虾、螃蟹、鸭肉、羊肉 |
| 蔬菜 | 17种 | 生菜沙拉、青菜、菠菜、西兰花、白菜、胡萝卜 |
| 水果 | 12种 | 苹果、香蕉、橙子、葡萄、西瓜、梨、桃子 |
| 主食 | 18种 | 米饭、面条、全麦面包、馒头、包子、饺子、粥 |
| 蛋类 | 3种 | 鸡蛋、鸭蛋、鹌鹑蛋 |
| 乳制品 | 5种 | 牛奶、酸奶、奶酪、奶粉、黄油 |
| 豆制品 | 4种 | 豆腐、豆浆、豆皮、腐竹 |
| 坚果零食 | 8种 | 花生、核桃、杏仁、瓜子、薯片、巧克力 |
| 外卖菜品 | 10种 | 宫保鸡丁、鱼香肉丝、麻婆豆腐、回锅肉 |
| 早餐 | 8种 | 豆浆、油条、包子、煎饼、玉米、红薯 |

**总计：105种食物**

**数据结构示例：**
```python
"鸡胸肉": {
    "category": "meat",
    "aliases": ["鸡肉", "白切鸡", "宫保鸡丁", "口水鸡", "辣子鸡"],
    "calories_per_100g": 165,
    "protein_per_100g": 31,
    "portions": [
        {"name": "掌心大小（薄切，约80g）", "weight": 80},
        {"name": "掌心大小（正常厚度，约120g）", "weight": 120},
        {"name": "掌心大小×1.5（厚切，约180g）", "weight": 180},
    ]
}
```

### 3. 优化AI提示词提高识别准确率 ✅

**文件修改：** `backend/app/services/ai_service.py`

**优化内容：**

**原有提示词：**
```
请识别这张图片中的食物，列出所有可见的食物。
要求：
1. 用逗号分隔多个食物名称
2. 名称要简洁
3. 不要回答烹饪方式或口感描述
```

**优化后提示词：**
```
请识别这张图片中的中式食物，列出所有可见的食物。

【重要】这是中国食物记录应用，请优先识别中式常见食物：
- 肉类：鸡胸肉、牛肉、猪肉、排骨、鱼、虾、羊肉等
- 主食：米饭、面条、饺子、馒头、包子、粥等
- 蔬菜：青菜、白菜、西兰花、菠菜、番茄、黄瓜等
- 豆制品：豆腐、豆浆、豆皮等
- 蛋类：鸡蛋、鸭蛋等

识别要求：
1. 用逗号分隔多个食物名称
2. 优先使用食物基础名称（如"鸡胸肉"而非"宫保鸡丁"）
3. 不要回答烹饪方式、口感描述或装饰物
4. 最多返回3个主要食物
```

**扩展食物名称映射：**
- 原有映射：约30个条目
- 优化后映射：约200+个条目
- 覆盖105种食物及其别名

**映射示例：**
```python
FOOD_NAME_MAPPING = {
    # 肉类
    "鸡胸肉": "鸡胸肉", "鸡肉": "鸡胸肉", "白切鸡": "鸡胸肉",
    "宫保鸡丁": "鸡胸肉", "口水鸡": "鸡胸肉", "辣子鸡": "鸡胸肉",
    # ... 200+ 映射条目
}
```

### 4. 前端集成待完成 ⏳

**需要前端开发人员实现：**

1. **Record.vue 修改**
   - 添加AI识别失败处理逻辑
   - 创建食物分类选择组件
   - 创建食物列表展示组件
   - 集成搜索功能

2. **推荐实现流程：**
   ```typescript
   // 当API返回400错误且code="RECOGNITION_FAILED"时
   if (error.code === "RECOGNITION_FAILED") {
     showFoodCategorySelector();
   }

   // 显示食物分类选择界面
   async function showFoodCategorySelector() {
     const categories = await api.getFoodCategories();
     // 渲染分类选项卡
   }

   // 用户选择分类后
   async function onCategorySelect(categoryKey: string) {
     const foods = await api.getFoodsByCategory(categoryKey);
     // 渲染食物列表
   }

   // 用户选择食物后
   async function onFoodSelect(foodName: string) {
     // 调用现有的份量选择流程
     const portions = await api.analyzeImage('', foodName); // 需后端支持
   }
   ```

---

## 完整输出文件路径

### 后端文件（修改）

| 文件路径 | 修改内容 |
|----------|----------|
| `backend/app/api/meal.py` | 新增3个食物分类相关API接口 |
| `backend/app/services/ai_service.py` | 优化AI提示词、扩展食物名称映射 |

### 后端文件（新建）

| 文件路径 | 说明 |
|----------|------|
| `backend/app/data/extended_food_database.py` | 扩展食物知识库（105种食物） |

### 文档文件（新建）

| 文件路径 | 说明 |
|----------|------|
| `AI_FAILURE_OPTIMIZATION_SUMMARY.md` | 本任务摘要文档 |

---

## 后续待办事项

### 必须完成（核心功能）

1. **前端Record.vue集成** - 实现AI识别失败后的备选流程UI
2. **数据库初始化脚本更新** - 将105种食物导入数据库

### 建议完成（体验优化）

1. **前端搜索功能** - 添加食物搜索输入框
2. **食物收藏功能** - 用户可收藏常用食物
3. **识别历史记录** - 记录用户选择的食物以便快速选择
4. **智能推荐优化** - 根据用户选择历史优化推荐

### 上线后优化

1. **用户反馈收集** - 收集识别失败案例
2. **AI模型微调** - 基于收集的数据优化识别准确率
3. **食物库持续扩展** - 添加更多地域特色食物

---

## 技术要点

### API接口说明

**1. 获取食物分类**
```http
GET /api/food-categories

Response:
{
  "categories": [
    {
      "key": "meat",
      "name": "肉类/禽类/鱼类",
      "icon": "🥩",
      "description": "高蛋白食物"
    }
  ]
}
```

**2. 获取分类下的食物**
```http
GET /api/foods-by-category/meat

Response:
{
  "category": {
    "key": "meat",
    "name": "肉类/禽类/鱼类",
    "icon": "🥩",
    "description": "高蛋白食物"
  },
  "foods": [
    {
      "name": "鸡胸肉",
      "category": "meat",
      "aliases": ["鸡肉", "白切鸡", "宫保鸡丁"],
      "calories_per_100g": 165,
      "protein_per_100g": 31,
      "portion_count": 4
    }
  ]
}
```

**3. 搜索食物**
```http
GET /api/food-search?q=鸡

Response:
[
  {
    "name": "鸡胸肉",
    "category": "meat",
    "aliases": ["鸡肉", "白切鸡"],
    "calories_per_100g": 165,
    "protein_per_100g": 31,
    "portion_count": 4
  }
]
```

### 错误码说明

| 错误码 | 说明 | 处理方式 |
|--------|------|----------|
| `RECOGNITION_FAILED` | AI识别失败 | 显示食物分类选择界面 |
| `FOOD_NOT_FOUND` | 识别的食物不在知识库 | 显示食物分类选择界面 |

### 前端集成示例

```typescript
// api/index.ts 新增接口
export interface CategoryInfo {
  key: string
  name: string
  icon: string
  description: string
}

export interface FoodItemInfo {
  name: string
  category: string
  aliases: string[]
  calories_per_100g: number
  protein_per_100g: number
  portion_count: number
}

// 获取食物分类
async function getFoodCategories(): Promise<CategoryInfo[]> {
  const response = await fetch(`${API_BASE_URL}/food-categories`)
  return (await response.json()).categories
}

// 获取分类下的食物
async function getFoodsByCategory(categoryKey: string): Promise<{category: CategoryInfo, foods: FoodItemInfo[]}> {
  const response = await fetch(`${API_BASE_URL}/foods-by-category/${categoryKey}`)
  return await response.json()
}

// 搜索食物
async function searchFoods(query: string): Promise<FoodItemInfo[]> {
  const response = await fetch(`${API_BASE_URL}/food-search?q=${encodeURIComponent(query)}`)
  return await response.json()
}
```

---

## 项目状态总结

### 已完成 ✅

- ✅ 食物知识库扩展至105种
- ✅ 后端API接口实现（3个新接口）
- ✅ AI提示词优化（中式食物识别）
- ✅ 食物名称映射扩展（200+条目）

### 待完成 ⏳

- ⏳ 前端Record.vue集成备选流程UI
- ⏳ 数据库初始化脚本更新
- ⏳ 集成测试验证

---

*文档版本: v1.1*
*生成日期: 2026-01-16*
*状态: ✅ 核心任务完成，前端集成待执行*
