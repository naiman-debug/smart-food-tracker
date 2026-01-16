# GLM API 集成测试指南

## 提供的测试密钥

```
API Key: 7ce400cc79454af49b6fd62ebc69e7ab.LiscGibdoY1Dzp4z
模型: glm-4.6v-flash (免费版)
```

---

## 快速测试方法

### 方法1：使用 Python 测试脚本

```bash
# 1. 进入后端目录
cd 智能食物记录/backend

# 2. 安装依赖
pip install httpx

# 3. 运行测试脚本
python test_glm_integration.py
```

**测试脚本已创建：** `backend/test_glm_integration.py`

---

### 方法2：使用 curl 测试

```bash
curl -X POST "https://open.bigmodel.cn/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer 7ce400cc79454af49b6fd62ebc69e7ab.LiscGibdoY1Dzp4z" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4.6v-flash",
    "messages": [
      {
        "role": "user",
        "content": "你好，请回复\"连接成功\""
      }
    ],
    "max_tokens": 50
  }'
```

**预期响应：**
```json
{
  "choices": [
    {
      "message": {
        "content": "连接成功"
      }
    }
  ]
}
```

---

### 方法3：配置后端服务测试

```bash
# 1. 配置环境变量
cd backend
# 创建 .env 文件
echo "GLM_API_KEY=7ce400cc79454af49b6fd62ebc69e7ab.LiscGibdoY1Dzp4z" > .env

# 2. 安装依赖
pip install -r requirements.txt

# 3. 启动服务
uvicorn app.main:app --reload

# 4. 查看日志
# 看到 "GLM未配置，使用模拟识别" 表示环境变量未生效
# 看到 "AI识别结果: xxx (使用真实AI: True)" 表示集成成功
```

---

## 验证集成成功的标志

### 启动日志

**集成成功：**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
INFO:     AI识别结果: 鸡胸肉 (使用真实AI: True)
```

**集成失败（降级）：**
```
INFO:     GLM未配置，使用模拟识别
INFO:     AI识别结果: 鸡胸肉 (使用真实AI: False)
```

---

## API 测试示例

### 使用 Postman / curl 测试 POST /api/analyze

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
  }'
```

**预期响应：**
```json
{
  "food_name": "鸡胸肉",
  "portion_options": [
    {
      "id": 2,
      "food_name": "鸡胸肉",
      "portion_name": "掌心大小（正常厚度，约120g）",
      "weight_grams": 120.0,
      "calories": 198.0,
      "protein": 37.0
    }
  ],
  "ai_used": true
}
```

---

## 常见问题排查

### 1. 状态码 401 - API密钥无效

**可能原因：**
- 密钥格式错误
- 密钥已过期/被撤销

**解决方法：**
```bash
# 重新获取API密钥
# 访问 https://open.bigmodel.cn/usercenter/apikeys
```

### 2. 状态码 429 - 请求频率超限

**可能原因：**
- 免费版配额已用完
- 请求过于频繁

**解决方法：**
- 等待一段时间后重试
- 升级到付费版本

### 3. 网络连接超时

**可能原因：**
- 网络问题
- API服务不可用

**解决方法：**
- 检查网络连接
- 系统会自动降级到模拟识别

---

## 测试报告模板

请完成测试后填写：

```markdown
| 测试项 | 结果 | 响应时间 | 备注 |
|--------|------|----------|------|
| API密钥验证 | ✅/❌ | ___ ms | |
| 文本识别测试 | ✅/❌ | ___ ms | |
| 图像识别测试 | ✅/❌ | ___ ms | |
| 名称映射功能 | ✅/❌ | - | |
| 错误处理测试 | ✅/❌ | - | |
| 降级机制测试 | ✅/❌ | - | |

测试日期: ___________
测试人: ___________
```

---

## 更新 GLM_INTEGRATION_LOG.md

测试完成后，请将测试结果同步到 `GLM_INTEGRATION_LOG.md` 文档。
