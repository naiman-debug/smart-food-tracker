# GLM 图像识别配置指南

## 快速开始

### 1. 获取智谱AI API密钥

1. 访问智谱AI开放平台：https://open.bigmodel.cn/
2. 注册/登录账号
3. 进入 API密钥管理：https://open.bigmodel.cn/usercenter/apikeys
4. 创建新的API Key
5. 复制生成的密钥（格式：`id.secret`）

### 2. 配置环境变量

在 `backend` 目录下创建 `.env` 文件：

```bash
# 复制示例配置文件
cp .env.example .env
```

编辑 `.env` 文件：

```bash
GLM_API_KEY=your_api_key_here
```

### 3. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

确保 `requirements.txt` 包含 `httpx>=0.25.0`

### 4. 启动服务

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. 验证配置

启动后检查控制台日志：

- ✅ **成功**: 看到 `INFO:     Application startup complete.` 且无错误
- ❌ **未配置**: 看到 `GLM未配置，使用模拟识别`
- ❌ **密钥无效**: 看到 `GLM API密钥无效`

---

## API使用示例

### cURL 测试

```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "image_base64": "base64_encoded_image_string"
  }'
```

### 响应示例

```json
{
  "food_name": "鸡胸肉",
  "portion_options": [
    {
      "id": 2,
      "food_name": "鸡胸肉",
      "portion_name": "掌心大小",
      "weight_grams": 120.0,
      "calories": 198.0,
      "protein": 37.0
    },
    {
      "id": 1,
      "food_name": "鸡胸肉",
      "portion_name": "拳头大小",
      "weight_grams": 80.0,
      "calories": 132.0,
      "protein": 24.7
    }
  ],
  "ai_used": true
}
```

---

## 高级配置

### 超时设置

默认超时30秒，可在 `ai_service.py` 中调整：

```python
async with httpx.AsyncClient(timeout=30.0) as client:
```

### 重试机制

当前版本不包含自动重试，降级到模拟识别。
如需添加重试，可修改 `analyze_image_with_glm` 方法。

### 日志级别

在 `app/api/meal.py` 中调整：

```python
logging.basicConfig(level=logging.DEBUG)  # 开发环境
logging.basicConfig(level=logging.INFO)   # 生产环境
```

---

## 故障排查

### 问题1：GLM未配置，使用模拟识别

**原因**: `GLM_API_KEY` 环境变量未设置

**解决**:
```bash
# 检查环境变量
echo $GLM_API_KEY

# 或在.env文件中确认
cat backend/.env
```

### 问题2：GLM API密钥无效

**原因**: API密钥格式错误或已失效

**解决**:
- 确认密钥格式为 `id.secret`
- 重新生成API密钥
- 检查密钥是否已启用

### 问题3：GLM API 请求超时

**原因**: 网络连接问题或API服务繁忙

**解决**:
- 检查网络连接
- 系统会自动降级到模拟识别
- 可考虑增加超时时间

### 问题4：识别结果为未知食物

**原因**: AI识别的食物不在知识库中

**解决**:
- 查看404响应中的 `available_foods` 列表
- 扩展 `VisualPortion` 表添加新食物
- 优化 `FOOD_NAME_MAPPING` 添加更多映射

---

## 开发调试

### 启用调试日志

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### 查看GLM原始响应

在 `analyze_image_with_glm` 方法中添加：

```python
logger.debug(f"GLM原始响应: {data}")
```

### 测试食物名称映射

```python
from app.services.ai_service import AIService

# 测试映射
print(AIService.normalize_food_name("宫保鸡丁"))  # 输出: 鸡胸肉
print(AIService.normalize_food_name("白米饭"))    # 输出: 米饭
```

---

## 生产部署

### 使用 .env 文件（推荐）

```bash
# 确保.env在.gitignore中
echo ".env" >> .gitignore

# 部署时在服务器上创建.env
vim /path/to/app/.env
```

### 使用系统环境变量

```bash
export GLM_API_KEY="your_api_key"
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Docker 部署

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# 环境变量通过docker-compose或docker run传入
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml
services:
  backend:
    build: ./backend
    environment:
      - GLM_API_KEY=${GLM_API_KEY}
    ports:
      - "8000:8000"
```

---

## 安全建议

1. **不要提交API密钥到版本控制**
   ```bash
   # .gitignore
   .env
   .env.local
   ```

2. **使用不同的密钥用于开发/生产**
   - 开发环境使用测试密钥
   - 生产环境使用正式密钥

3. **定期轮换API密钥**
   - 每季度更换一次
   - 怀疑泄露时立即更换

4. **监控API使用量**
   - 在智谱AI控制台查看调用统计
   - 设置用量告警

---

## 更新日志

| 日期 | 版本 | 变更内容 |
|------|------|----------|
| 2026-01-16 | v1.0 | 初始版本 |

---

## 联系支持

- **智谱AI技术支持**: https://open.bigmodel.cn/support
- **GLM开发文档**: https://docs.bigmodel.cn/
- **GitHub Issues**: 项目仓库的Issues页面
