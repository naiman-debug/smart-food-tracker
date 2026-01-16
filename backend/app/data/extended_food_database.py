"""
扩展食物知识库数据
目标：80-100种常见中式日常食物
"""
from typing import List, Dict

# 扩展的食物知识库数据
EXTENDED_FOOD_DATABASE = {
    # ========== 肉类/禽类/鱼类 (20种) ==========
    "鸡胸肉": {
        "category": "meat",
        "aliases": ["鸡肉", "白切鸡", "宫保鸡丁", "口水鸡", "辣子鸡", "鸡柳", "鸡排"],
        "calories_per_100g": 165,
        "protein_per_100g": 31,
        "portions": [
            {"name": "掌心大小（薄切，约80g）", "weight": 80},
            {"name": "掌心大小（正常厚度，约120g）", "weight": 120},
            {"name": "掌心大小×1.5（厚切，约180g）", "weight": 180},
            {"name": "信用卡厚度（约50g）", "weight": 50},
        ]
    },
    "牛肉": {
        "category": "meat",
        "aliases": ["牛排", "肥牛", "瘦牛肉", "红烧牛肉"],
        "calories_per_100g": 250,
        "protein_per_100g": 26,
        "portions": [
            {"name": "掌心大小（薄切，约80g）", "weight": 80},
            {"name": "掌心大小（正常厚度，约120g）", "weight": 120},
            {"name": "掌心大小×1.5（厚切，约180g）", "weight": 180},
        ]
    },
    "牛排": {
        "category": "meat",
        "aliases": ["西冷牛排", "菲力牛排", "肋眼牛排"],
        "calories_per_100g": 271,
        "protein_per_100g": 25,
        "portions": [
            {"name": "掌心大小（约150g）", "weight": 150},
            {"name": "掌心大小×1.5（约225g）", "weight": 225},
        ]
    },
    "猪肉": {
        "category": "meat",
        "aliases": ["瘦肉", "五花肉", "梅花肉", "里脊肉"],
        "calories_per_100g": 143,
        "protein_per_100g": 20,
        "portions": [
            {"name": "掌心大小（约100g）", "weight": 100},
            {"name": "掌心大小×1.5（约150g）", "weight": 150},
        ]
    },
    "红烧肉": {
        "category": "meat",
        "aliases": ["东坡肉", "扣肉", "红烧五花肉"],
        "calories_per_100g": 320,
        "protein_per_100g": 15,
        "portions": [
            {"name": "掌心大小（约100g）", "weight": 100},
            {"name": "掌心大小×1.5（约150g）", "weight": 150},
        ]
    },
    "排骨": {
        "category": "meat",
        "aliases": ["猪排", " ribs", "糖醋排骨"],
        "calories_per_100g": 260,
        "protein_per_100g": 17,
        "portions": [
            {"name": "两块（约100g）", "weight": 100},
            {"name": "三块（约150g）", "weight": 150},
        ]
    },
    "鱼": {
        "category": "meat",
        "aliases": ["清蒸鱼", "红烧鱼", "鲈鱼", "草鱼", "鲫鱼"],
        "calories_per_100g": 140,
        "protein_per_100g": 20,
        "portions": [
            {"name": "掌心大小（约100g）", "weight": 100},
            {"name": "掌心大小×1.5（约150g）", "weight": 150},
        ]
    },
    "虾": {
        "category": "meat",
        "aliases": ["白灼虾", "油焖大虾", "虾仁", "基围虾"],
        "calories_per_100g": 85,
        "protein_per_100g": 20,
        "portions": [
            {"name": "一手抓（约80g）", "weight": 80},
            {"name": "双手一捧（约150g）", "weight": 150},
        ]
    },
    "螃蟹": {
        "category": "meat",
        "aliases": ["大闸蟹", "梭子蟹", "毛蟹"],
        "calories_per_100g": 95,
        "protein_per_100g": 18,
        "portions": [
            {"name": "一只（约150g）", "weight": 150},
            {"name": "一只×1.5（约225g）", "weight": 225},
        ]
    },
    "鸭肉": {
        "category": "meat",
        "aliases": ["烤鸭", "盐水鸭", "酱鸭"],
        "calories_per_100g": 240,
        "protein_per_100g": 19,
        "portions": [
            {"name": "掌心大小（约120g）", "weight": 120},
            {"name": "掌心大小×1.5（约180g）", "weight": 180},
        ]
    },
    "羊肉": {
        "category": "meat",
        "aliases": ["羊肉串", "羊排", "红烧羊肉"],
        "calories_per_100g": 203,
        "protein_per_100g": 20,
        "portions": [
            {"name": "掌心大小（约100g）", "weight": 100},
            {"name": "掌心大小×1.5（约150g）", "weight": 150},
        ]
    },
    "培根": {
        "category": "meat",
        "aliases": ["烟肉", "熏肉", "咸肉"],
        "calories_per_100g": 540,
        "protein_per_100g": 10,
        "portions": [
            {"name": "一片（约15g）", "weight": 15},
            {"name": "两片（约30g）", "weight": 30},
        ]
    },
    "火腿": {
        "category": "meat",
        "aliases": ["火腿肠", "午餐肉"],
        "calories_per_100g": 320,
        "protein_per_100g": 20,
        "portions": [
            {"name": "一片（约20g）", "weight": 20},
            {"name": "三片（约60g）", "weight": 60},
        ]
    },
    "香肠": {
        "category": "meat",
        "aliases": ["腊肠", "广式腊肠", "红肠"],
        "calories_per_100g": 350,
        "protein_per_100g": 12,
        "portions": [
            {"name": "一根（约50g）", "weight": 50},
            {"name": "一根×1.5（约75g）", "weight": 75},
        ]
    },
    "鸡翅": {
        "category": "meat",
        "aliases": ["烤鸡翅", "可乐鸡翅", "炸鸡翅"],
        "calories_per_100g": 200,
        "protein_per_100g": 17,
        "portions": [
            {"name": "一只（约60g）", "weight": 60},
            {"name": "两只（约120g）", "weight": 120},
        ]
    },
    "鸡腿": {
        "category": "meat",
        "aliases": ["烤鸡腿", "炸鸡腿"],
        "calories_per_100g": 180,
        "protein_per_100g": 18,
        "portions": [
            {"name": "一只（约100g）", "weight": 100},
            {"name": "一只×1.5（约150g）", "weight": 150},
        ]
    },
    "肉丸": {
        "category": "meat",
        "aliases": ["牛肉丸", "鱼丸", "虾丸"],
        "calories_per_100g": 220,
        "protein_per_100g": 15,
        "portions": [
            {"name": "三颗（约50g）", "weight": 50},
            {"name": "六颗（约100g）", "weight": 100},
        ]
    },
    "火锅丸子": {
        "category": "meat",
        "aliases": ["撒尿牛丸", "贡丸", "鱼豆腐"],
        "calories_per_100g": 200,
        "protein_per_100g": 12,
        "portions": [
            {"name": "三颗（约50g）", "weight": 50},
            {"name": "六颗（约100g）", "weight": 100},
        ]
    },

    # ========== 蔬菜类 (15种) ==========
    "生菜沙拉": {
        "category": "vegetable",
        "aliases": ["沙拉", "蔬菜沙拉"],
        "calories_per_100g": 20,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "一手抓起的量（约30g）", "weight": 30},
            {"name": "双手一捧（约80g）", "weight": 80},
            {"name": "双手一捧×1.5（约120g）", "weight": 120},
        ]
    },
    "青菜": {
        "category": "vegetable",
        "aliases": ["小白菜", "油菜", "绿叶菜"],
        "calories_per_100g": 25,
        "protein_per_100g": 2,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
            {"name": "双手一捧×1.5（约150g）", "weight": 150},
        ]
    },
    "菠菜": {
        "category": "vegetable",
        "aliases": ["凉拌菠菜", "清炒菠菜"],
        "calories_per_100g": 23,
        "protein_per_100g": 2.9,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
        ]
    },
    "西兰花": {
        "category": "vegetable",
        "aliases": ["西蓝花", "花椰菜"],
        "calories_per_100g": 34,
        "protein_per_100g": 2.8,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
        ]
    },
    "白菜": {
        "category": "vegetable",
        "aliases": ["大白菜", "娃娃菜", "圆白菜"],
        "calories_per_100g": 17,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
            {"name": "双手一捧×1.5（约150g）", "weight": 150},
        ]
    },
    "胡萝卜": {
        "category": "vegetable",
        "aliases": ["红萝卜", "炒胡萝卜"],
        "calories_per_100g": 41,
        "protein_per_100g": 0.9,
        "portions": [
            {"name": "一根（约80g）", "weight": 80},
            {"name": "一根×1.5（约120g）", "weight": 120},
        ]
    },
    "番茄": {
        "category": "vegetable",
        "aliases": ["西红柿", "番茄炒蛋", "番茄"],
        "calories_per_100g": 18,
        "protein_per_100g": 0.9,
        "portions": [
            {"name": "一个（约100g）", "weight": 100},
            {"name": "一个×1.5（约150g）", "weight": 150},
        ]
    },
    "黄瓜": {
        "category": "vegetable",
        "aliases": ["凉拌黄瓜", "拍黄瓜"],
        "calories_per_100g": 16,
        "protein_per_100g": 0.8,
        "portions": [
            {"name": "一根（约100g）", "weight": 100},
            {"name": "一根×1.5（约150g）", "weight": 150},
        ]
    },
    "土豆": {
        "category": "vegetable",
        "aliases": ["马铃薯", "土豆丝", "炸土豆", "烤土豆"],
        "calories_per_100g": 77,
        "protein_per_100g": 2,
        "portions": [
            {"name": "拳头大小（约150g）", "weight": 150},
            {"name": "拳头大小×1.5（约225g）", "weight": 225},
        ]
    },
    "茄子": {
        "category": "vegetable",
        "aliases": ["烤茄子", "鱼香茄子", "地三鲜"],
        "calories_per_100g": 25,
        "protein_per_100g": 1,
        "portions": [
            {"name": "半根（约100g）", "weight": 100},
        ]
    },
    "豆角": {
        "category": "vegetable",
        "aliases": ["四季豆", "长豆角", "干煸豆角"],
        "calories_per_100g": 35,
        "protein_per_100g": 2,
        "portions": [
            {"name": "双手一捧（约80g）", "weight": 80},
            {"name": "双手一捧×1.5（约120g）", "weight": 120},
        ]
    },
    "莲藕": {
        "category": "vegetable",
        "aliases": ["藕片", "糖醋藕"],
        "calories_per_100g": 44,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "两片（约80g）", "weight": 80},
            {"name": "三片（约120g）", "weight": 120},
        ]
    },
    "菌菇": {
        "category": "vegetable",
        "aliases": ["香菇", "平菇", "金针菇", "蘑菇"],
        "calories_per_100g": 22,
        "protein_per_100g": 3,
        "portions": [
            {"name": "一手抓（约50g）", "weight": 50},
            {"name": "双手一捧（约100g）", "weight": 100},
        ]
    },
    "海带": {
        "category": "vegetable",
        "aliases": ["凉拌海带", "海带丝"],
        "calories_per_100g": 25,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "一小盘（约50g）", "weight": 50},
        ]
    },
    "豆芽": {
        "category": "vegetable",
        "aliases": ["绿豆芽", "黄豆芽"],
        "calories_per_100g": 30,
        "protein_per_100g": 3,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
        ]
    },
    "冬瓜": {
        "category": "vegetable",
        "aliases": ["冬瓜汤"],
        "calories_per_100g": 13,
        "protein_per_100g": 0.4,
        "portions": [
            {"name": "一碗（约150g）", "weight": 150},
        ]
    },
    "南瓜": {
        "category": "vegetable",
        "aliases": ["蒸南瓜", "南瓜汤"],
        "calories_per_100g": 26,
        "protein_per_100g": 1,
        "portions": [
            {"name": "一碗（约150g）", "weight": 150},
        ]
    },

    # ========== 水果类 (12种) ==========
    "苹果": {
        "category": "fruit",
        "aliases": ["红富士", "青苹果", "苹果"],
        "calories_per_100g": 52,
        "protein_per_100g": 0.3,
        "portions": [
            {"name": "网球大小（小苹果，约80g）", "weight": 80},
            {"name": "拳头大小（正常苹果，约150g）", "weight": 150},
            {"name": "拳头大小×1.5（大苹果，约225g）", "weight": 225},
        ]
    },
    "香蕉": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 89,
        "protein_per_100g": 1.1,
        "portions": [
            {"name": "一根（小，约80g）", "weight": 80},
            {"name": "一根（正常，约120g）", "weight": 120},
        ]
    },
    "橙子": {
        "category": "fruit",
        "aliases": ["橙子", "橘子", "砂糖橘"],
        "calories_per_100g": 47,
        "protein_per_100g": 0.9,
        "portions": [
            {"name": "拳头大小（约150g）", "weight": 150},
        ]
    },
    "葡萄": {
        "category": "fruit",
        "aliases": ["提子", "巨峰葡萄"],
        "calories_per_100g": 69,
        "protein_per_100g": 0.7,
        "portions": [
            {"name": "一小串（约80g）", "weight": 80},
            {"name": "一小串×1.5（约120g）", "weight": 120},
        ]
    },
    "西瓜": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 30,
        "protein_per_100g": 0.6,
        "portions": [
            {"name": "一片（约200g）", "weight": 200},
            {"name": "一片×1.5（约300g）", "weight": 300},
        ]
    },
    "梨": {
        "category": "fruit",
        "aliases": ["香梨", "雪梨"],
        "calories_per_100g": 57,
        "protein_per_100g": 0.4,
        "portions": [
            {"name": "拳头大小（约150g）", "weight": 150},
        ]
    },
    "桃子": {
        "category": "fruit",
        "aliases": ["水蜜桃", "油桃"],
        "calories_per_100g": 41,
        "protein_per_100g": 0.5,
        "portions": [
            {"name": "拳头大小（约150g）", "weight": 150},
        ]
    },
    "猕猴桃": {
        "category": "fruit",
        "aliases": ["奇异果", "kiwi"],
        "calories_per_100g": 61,
        "protein_per_100g": 1,
        "portions": [
            {"name": "一个（约80g）", "weight": 80},
            {"name": "一个×1.5（约120g）", "weight": 120},
        ]
    },
    "芒果": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 60,
        "protein_per_100g": 0.8,
        "portions": [
            {"name": "半个（约100g）", "weight": 100},
            {"name": "一个（约200g）", "weight": 200},
        ]
    },
    "草莓": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 32,
        "protein_per_100g": 0.7,
        "portions": [
            {"name": "5颗（约80g）", "weight": 80},
            {"name": "8颗（约120g）", "weight": 120},
        ]
    },
    "蓝莓": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 57,
        "protein_per_100g": 0.7,
        "portions": [
            {"name": "一小盒（约80g）", "weight": 80},
            {"name": "一小盒×1.5（约120g）", "weight": 120},
        ]
    },
    "樱桃": {
        "category": "fruit",
        "aliases": [],
        "calories_per_100g": 50,
        "protein_per_100g": 1,
        "portions": [
            {"name": "一把（约50g）", "weight": 50},
            {"name": "一把×1.5（约75g）", "weight": 75},
        ]
    },

    # ========== 主食类 (18种) ==========
    "米饭": {
        "category": "staple",
        "aliases": ["白米饭", "蒸饭", "粳米"],
        "calories_per_100g": 130,
        "protein_per_100g": 2.7,
        "portions": [
            {"name": "一小碗（约100g）", "weight": 100},
            {"name": "平时饭碗的一碗（约150g）", "weight": 150},
            {"name": "平时饭碗的一碗半（约225g）", "weight": 225},
        ]
    },
    "面条": {
        "category": "staple",
        "aliases": ["拉面", "汤面", "炒面", "干面"],
        "calories_per_100g": 140,
        "protein_per_100g": 4,
        "portions": [
            {"name": "一小碗（约100g）", "weight": 100},
            {"name": "平时饭碗的一碗（约150g）", "weight": 150},
        ]
    },
    "意大利面": {
        "category": "staple",
        "aliases": ["意面", "pasta", "肉酱面"],
        "calories_per_100g": 131,
        "protein_per_100g": 5,
        "portions": [
            {"name": "一小碗（约100g）", "weight": 100},
            {"name": "一小碗×1.5（约150g）", "weight": 150},
        ]
    },
    "全麦面包": {
        "category": "staple",
        "aliases": ["全麦吐司", "黑麦面包"],
        "calories_per_100g": 250,
        "protein_per_100g": 10,
        "portions": [
            {"name": "一片（约30g）", "weight": 30},
            {"name": "两片（约60g）", "weight": 60},
        ]
    },
    "白面包": {
        "category": "staple",
        "aliases": ["吐司", "切片面包", "三明治面包"],
        "calories_per_100g": 265,
        "protein_per_100g": 9,
        "portions": [
            {"name": "一片（约30g）", "weight": 30},
            {"name": "两片（约60g）", "weight": 60},
        ]
    },
    "馒头": {
        "category": "staple",
        "aliases": ["蒸馒头", "白馒头", "花卷"],
        "calories_per_100g": 220,
        "protein_per_100g": 7,
        "portions": [
            {"name": "半个（约50g）", "weight": 50},
            {"name": "一个（约100g）", "weight": 100},
        ]
    },
    "包子": {
        "category": "staple",
        "aliases": ["肉包", "菜包", "豆沙包"],
        "calories_per_100g": 230,
        "protein_per_100g": 7,
        "portions": [
            {"name": "一个（约80g）", "weight": 80},
            {"name": "一个×1.5（约120g）", "weight": 120},
        ]
    },
    "饺子": {
        "category": "staple",
        "aliases": ["水饺", "煎饺", "蒸饺"],
        "calories_per_100g": 250,
        "protein_per_100g": 8,
        "portions": [
            {"name": "8个（约150g）", "weight": 150},
            {"name": "12个（约225g）", "weight": 225},
        ]
    },
    "馄饨": {
        "category": "staple",
        "aliases": ["云吞", "抄手"],
        "calories_per_100g": 240,
        "protein_per_100g": 8,
        "portions": [
            {"name": "一小碗（约150g）", "weight": 150},
            {"name": "一小碗×1.5（约225g）", "weight": 225},
        ]
    },
    "煎饼": {
        "category": "staple",
        "aliases": ["煎饼果子", "鸡蛋饼"],
        "calories_per_100g": 250,
        "protein_per_100g": 8,
        "portions": [
            {"name": "半张（约100g）", "weight": 100},
            {"name": "一张（约200g）", "weight": 200},
        ]
    },
    "油条": {
        "category": "staple",
        "aliases": [],
        "calories_per_100g": 390,
        "protein_per_100g": 6,
        "portions": [
            {"name": "半根（约60g）", "weight": 60},
            {"name": "一根（约120g）", "weight": 120},
        ]
    },
    "粥": {
        "category": "staple",
        "aliases": ["白粥", "小米粥", "皮蛋瘦肉粥"],
        "calories_per_100g": 60,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "一小碗（约150g）", "weight": 150},
            {"name": "一小碗×1.5（约225g）", "weight": 225},
        ]
    },
    "年糕": {
        "category": "staple",
        "aliases": ["炒年糕", "糖年糕"],
        "calories_per_100g": 154,
        "protein_per_100g": 3,
        "portions": [
            {"name": "一片（约50g）", "weight": 50},
            {"name": "两片（约100g）", "weight": 100},
        ]
    },
    "粽子": {
        "category": "staple",
        "aliases": ["肉粽", "蛋黄粽", "豆沙粽"],
        "calories_per_100g": 200,
        "protein_per_100g": 5,
        "portions": [
            {"name": "半个（约75g）", "weight": 75},
            {"name": "一个（约150g）", "weight": 150},
        ]
    },
    "烧麦": {
        "category": "staple",
        "aliases": ["烧卖"],
        "calories_per_100g": 230,
        "protein_per_100g": 8,
        "portions": [
            {"name": "3个（约75g）", "weight": 75},
            {"name": "5个（约125g）", "weight": 125},
        ]
    },
    "炒饭": {
        "category": "staple",
        "aliases": ["蛋炒饭", "扬州炒饭", "海鲜炒饭"],
        "calories_per_100g": 160,
        "protein_per_100g": 5,
        "portions": [
            {"name": "一小碗（约150g）", "weight": 150},
            {"name": "一小碗×1.5（约225g）", "weight": 225},
        ]
    },
    "炒面": {
        "category": "staple",
        "aliases": ["蛋炒面", "肉丝炒面"],
        "calories_per_100g": 165,
        "protein_per_100g": 6,
        "portions": [
            {"name": "一小碗（约150g）", "weight": 150},
        ]
    },

    # ========== 蛋类 (3种) ==========
    "鸡蛋": {
        "category": "egg",
        "aliases": ["水煮蛋", "煎蛋", "炒蛋", "西红柿炒鸡蛋", "鸡蛋羹"],
        "calories_per_100g": 155,
        "protein_per_100g": 13,
        "portions": [
            {"name": "水煮蛋1个（约50g）", "weight": 50},
            {"name": "煎蛋1个（约60g）", "weight": 60},
        ]
    },
    "鸭蛋": {
        "category": "egg",
        "aliases": ["咸鸭蛋", "皮蛋"],
        "calories_per_100g": 180,
        "protein_per_100g": 13,
        "portions": [
            {"name": "水煮蛋1个（约60g）", "weight": 60},
        ]
    },
    "鹌鹑蛋": {
        "category": "egg",
        "aliases": ["卤蛋", "虎皮蛋"],
        "calories_per_100g": 160,
        "protein_per_100g": 13,
        "portions": [
            {"name": "3个（约60g）", "weight": 60},
            {"name": "5个（约100g）", "weight": 100},
        ]
    },

    # ========== 乳制品类 (5种) ==========
    "牛奶": {
        "category": "dairy",
        "aliases": ["纯牛奶", "鲜奶"],
        "calories_per_100g": 54,
        "protein_per_100g": 3,
        "portions": [
            {"name": "一小杯（约150ml）", "weight": 150},
            {"name": "一杯（约250ml）", "weight": 250},
        ]
    },
    "酸奶": {
        "category": "dairy",
        "aliases": ["酸牛奶", "发酵乳"],
        "calories_per_100g": 60,
        "protein_per_100g": 4,
        "portions": [
            {"name": "小杯（约100g）", "weight": 100},
            {"name": "一杯（约150g）", "weight": 150},
        ]
    },
    "奶酪": {
        "category": "dairy",
        "aliases": ["芝士", "起司", "奶油芝士"],
        "calories_per_100g": 402,
        "protein_per_100g": 25,
        "portions": [
            {"name": "一小块（约20g）", "weight": 20},
            {"name": "一小块×2（约40g）", "weight": 40},
        ]
    },
    "奶粉": {
        "category": "dairy",
        "aliases": ["牛奶粉"],
        "calories_per_100g": 500,
        "protein_per_100g": 20,
        "portions": [
            {"name": "一勺（约15g）", "weight": 15},
            {"name": "两勺（约30g）", "weight": 30},
        ]
    },
    "黄油": {
        "category": "dairy",
        "aliases": ["黄油", "奶油"],
        "calories_per_100g": 720,
        "protein_per_100g": 0.9,
        "portions": [
            {"name": "一小块（约10g）", "weight": 10},
            {"name": "一小块×2（约20g）", "weight": 20},
        ]
    },

    # ========== 豆制品类 (4种) ==========
    "豆腐": {
        "category": "soy",
        "aliases": ["嫩豆腐", "老豆腐", "北豆腐"],
        "calories_per_100g": 76,
        "protein_per_100g": 8,
        "portions": [
            {"name": "掌心大小（约100g）", "weight": 100},
            {"name": "掌心大小×1.5（约150g）", "weight": 150},
        ]
    },
    "豆浆": {
        "category": "soy",
        "aliases": ["豆奶", "生磨豆浆"],
        "calories_per_100g": 35,
        "protein_per_100g": 3,
        "portions": [
            {"name": "一杯（约250ml）", "weight": 250},
        ]
    },
    "豆皮": {
        "category": "soy",
        "aliases": ["腐竹", "油皮"],
        "calories_per_100g": 230,
        "protein_per_100g": 20,
        "portions": [
            {"name": "一张（约10g）", "weight": 10},
            {"name": "三张（约30g）", "weight": 30},
        ]
    },
    "腐竹": {
        "category": "soy",
        "aliases": ["干腐竹"],
        "calories_per_100g": 460,
        "protein_per_100g": 40,
        "portions": [
            {"name": "一小把（约20g）", "weight": 20},
            {"name": "一小把×2（约40g）", "weight": 40},
        ]
    },

    # ========== 坚果零食类 (8种) ==========
    "花生": {
        "category": "snack",
        "aliases": ["炒花生", "煮花生"],
        "calories_per_100g": 570,
        "protein_per_100g": 25,
        "portions": [
            {"name": "一小把（约20g）", "weight": 20},
            {"name": "一小把×2（约40g）", "weight": 40},
        ]
    },
    "核桃": {
        "category": "snack",
        "aliases": ["胡桃"],
        "calories_per_100g": 650,
        "protein_per_100g": 15,
        "portions": [
            {"name": "两个（约20g）", "weight": 20},
            {"name": "四个（约40g）", "weight": 40},
        ]
    },
    "杏仁": {
        "category": "snack",
        "aliases": ["巴旦木"],
        "calories_per_100g": 579,
        "protein_per_100g": 21,
        "portions": [
            {"name": "一小把（约15g）", "weight": 15},
            {"name": "一小把×2（约30g）", "weight": 30},
        ]
    },
    "瓜子": {
        "category": "snack",
        "aliases": ["葵花籽", "西瓜子"],
        "calories_per_100g": 560,
        "protein_per_100g": 20,
        "portions": [
            {"name": "一小把（约20g）", "weight": 20},
            {"name": "一小把×2（约40g）", "weight": 40},
        ]
    },
    "薯片": {
        "category": "snack",
        "aliases": [" potato chips"],
        "calories_per_100g": 540,
        "protein_per_100g": 7,
        "portions": [
            {"name": "一小包（约30g）", "weight": 30},
            {"name": "一小包×2（约60g）", "weight": 60},
        ]
    },
    "薯条": {
        "category": "snack",
        "aliases": ["french fries"],
        "calories_per_100g": 320,
        "protein_per_100g": 3,
        "portions": [
            {"name": "小份（约80g）", "weight": 80},
            {"name": "中份（约120g）", "weight": 120},
        ]
    },
    "爆米花": {
        "category": "snack",
        "aliases": [],
        "calories_per_100g": 387,
        "protein_per_100g": 13,
        "portions": [
            {"name": "一小杯（约30g）", "weight": 30},
            {"name": "一大杯（约80g）", "weight": 80},
        ]
    },
    "巧克力": {
        "category": "snack",
        "aliases": ["黑巧克力", "牛奶巧克力"],
        "calories_per_100g": 546,
        "protein_per_100g": 5,
        "portions": [
            {"name": "一小块（约15g）", "weight": 15},
            {"name": "一小块×2（约30g）", "weight": 30},
        ]
    },

    # ========== 外卖常见菜品 (10种) ==========
    "宫保鸡丁": {
        "category": "takeout",
        "aliases": ["花生鸡丁"],
        "calories_per_100g": 180,
        "protein_per_100g": 12,
        "portions": [
            {"name": "平时饭碗的一碗半（约200g）", "weight": 200},
        ]
    },
    "鱼香肉丝": {
        "category": "takeout",
        "aliases": ["鱼香肉丝"],
        "calories_per_100g": 150,
        "protein_per_100g": 8,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "麻婆豆腐": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 120,
        "protein_per_100g": 7,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "回锅肉": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 250,
        "protein_per_100g": 12,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "糖醋排骨": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 280,
        "protein_per_100g": 15,
        "portions": [
            {"name": "平时饭碗的一碗（约150g）", "weight": 150},
        ]
    },
    "红烧肉": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 320,
        "protein_per_100g": 15,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "水煮鱼": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 100,
        "protein_per_100g": 18,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "清炒时蔬": {
        "category": "takeout",
        "aliases": ["时蔬", "青菜"],
        "calories_per_100g": 40,
        "protein_per_100g": 2,
        "portions": [
            {"name": "双手一捧（约100g）", "weight": 100},
        ]
    },
    "蛋炒饭": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 160,
        "protein_per_100g": 5,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },
    "扬州炒饭": {
        "category": "takeout",
        "aliases": [],
        "calories_per_100g": 170,
        "protein_per_100g": 6,
        "portions": [
            {"name": "平时饭碗的一碗（约200g）", "weight": 200},
        ]
    },

    # ========== 早餐常见 (8种) ==========
    "豆浆": {
        "category": "breakfast",
        "aliases": [],
        "calories_per_100g": 35,
        "protein_per_100g": 3,
        "portions": [
            {"name": "一杯（约250ml）", "weight": 250},
        ]
    },
    "油条": {
        "category": "breakfast",
        "aliases": [],
        "calories_per_100g": 390,
        "protein_per_100g": 6,
        "portions": [
            {"name": "半根（约60g）", "weight": 60},
            {"name": "一根（约120g）", "weight": 120},
        ]
    },
    "包子": {
        "category": "breakfast",
        "aliases": ["肉包", "菜包"],
        "calories_per_100g": 230,
        "protein_per_100g": 7,
        "portions": [
            {"name": "一个（约80g）", "weight": 80},
            {"name": "一个×1.5（约120g）", "weight": 120},
        ]
    },
    "煎饼": {
        "category": "breakfast",
        "aliases": ["煎饼果子"],
        "calories_per_100g": 250,
        "protein_per_100g": 8,
        "portions": [
            {"name": "半张（约100g）", "weight": 100},
            {"name": "一张（约200g）", "weight": 200},
        ]
    },
    "烧麦": {
        "category": "breakfast",
        "aliases": [],
        "calories_per_100g": 230,
        "protein_per_100g": 8,
        "portions": [
            {"name": "3个（约75g）", "weight": 75},
            {"name": "5个（约125g）", "weight": 125},
        ]
    },
    "粥": {
        "category": "breakfast",
        "aliases": ["白粥", "小米粥", "皮蛋瘦肉粥"],
        "calories_per_100g": 60,
        "protein_per_100g": 1.5,
        "portions": [
            {"name": "一小碗（约150g）", "weight": 150},
            {"name": "一小碗×1.5（约225g）", "weight": 225},
        ]
    },
    "玉米": {
        "category": "breakfast",
        "aliases": ["煮玉米", "烤玉米"],
        "calories_per_100g": 86,
        "protein_per_100g": 3,
        "portions": [
            {"name": "半根（约100g）", "weight": 100},
            {"name": "一根（约200g）", "weight": 200},
        ]
    },
    "红薯": {
        "category": "breakfast",
        "aliases": ["番薯", "烤红薯"],
        "calories_per_100g": 86,
        "protein_per_100g": 1.6,
        "portions": [
            {"name": "拳头大小（约150g）", "weight": 150},
            {"name": "拳头大小×1.5（约225g）", "weight": 225},
        ]
    },
}


# 食物分类映射表
FOOD_CATEGORIES = {
    "meat": {
        "name": "肉类/禽类/鱼类",
        "icon": "🥩",
        "description": "高蛋白食物"
    },
    "vegetable": {
        "name": "蔬菜",
        "icon": "🥬",
        "description": "维生素和纤维"
    },
    "fruit": {
        "name": "水果",
        "icon": "🍎",
        "description": "天然甜味"
    },
    "staple": {
        "name": "主食",
        "icon": "🍚�",
        "description": "碳水化合物"
    },
    "egg": {
        "name": "蛋类",
        "icon": "🥚",
        "description": "优质蛋白"
    },
    "dairy": {
        "name": "乳制品",
        "icon": "🥛",
        "description": "钙质补充"
    },
    "soy": {
        "name": "豆制品",
        "icon": "🫘",
        "description": "植物蛋白"
    },
    "snack": {
        "name": "坚果零食",
        "icon": "🥜",
        "description": "适量享用"
    },
    "takeout": {
        "name": "外卖菜品",
        "icon": "🍜",
        "description": "常见外卖"
    },
    "breakfast": {
        "name": "早餐",
        "icon": "🌅",
        "description": "早餐必备"
    },
}
