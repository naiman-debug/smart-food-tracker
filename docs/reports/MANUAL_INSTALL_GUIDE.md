# 手动安装指南

> 智能食物记录 App - 详细的手动安装步骤

---

## 目录

1. [环境要求](#1-环境要求)
2. [安装Python依赖](#2-安装python依赖)
3. [安装Node.js依赖](#3-安装nodejs依赖)
4. [初始化数据库](#4-初始化数据库)
5. [启动服务](#5-启动服务)
6. [常见问题解决](#6-常见问题解决)

---

## 1. 环境要求

### 必需软件

| 软件 | 版本要求 | 下载地址 |
|------|----------|----------|
| Python | 3.8+ | https://www.python.org/downloads/ |
| Node.js | 14+ | https://nodejs.org/ |

### 验证环境

打开命令提示符（CMD）或PowerShell，输入：

```bash
python --version
node --version
npm --version
```

---

## 2. 安装Python依赖

### 解决编码问题的方法

#### 方法1：使用UTF-8代码页（推荐）

```bash
# 1. 切换到UTF-8代码页
chcp 65001

# 2. 进入backend目录
cd 智能食物记录\backend

# 3. 升级pip
python -m pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt
```

#### 方法2：逐个安装包

如果上面的方法失败，可以逐个安装：

```bash
cd 智能食物记录\backend

pip install fastapi
pip install uvicorn[standard]
pip install sqlalchemy
pip install pydantic
pip install python-dotenv
pip install httpx
```

#### 方法3：使用国内镜像源

如果下载速度慢，使用清华源：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 验证安装

```bash
python -c "import fastapi, uvicorn, sqlalchemy; print('OK')"
```

如果显示 "OK"，说明安装成功。

---

## 3. 安装Node.js依赖

### 安装步骤

```bash
# 1. 进入frontend目录
cd 智能食物记录\frontend

# 2. 安装依赖
npm install
```

### 使用国内镜像（可选）

如果下载速度慢，使用淘宝镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

### 验证安装

检查 `node_modules` 文件夹是否存在且包含文件。

---

## 4. 初始化数据库

### 数据库初始化顺序

数据库初始化分为两步：**创建表结构** → **导入食物数据**

#### Step 1: 创建数据库表

```bash
cd 智能食物记录\backend
python create_tables.py
```

**预期输出：**
```
╔════════════════════════════════════════════════╗
║   Smart Food Tracker - Database Tables        ║
║                    Creation Script             ║
╚════════════════════════════════════════════════╝

============================================================
Step 1: Importing Models
============================================================

○ Importing all database models...
✓ Models imported successfully

============================================================
Step 2: Tables to Create
============================================================

○   - visual_portions
○   - meal_records
○   - daily_goals

============================================================
Step 3: Creating Tables
============================================================

✓ All database tables created successfully

============================================================
Step 4: Verification
============================================================

✓ Verified 3 tables in database:
  ○   - visual_portions
  ○   - meal_records
  ○   - daily_goals

✓ All required tables exist
```

#### Step 2: 导入食物数据（105种食物）

```bash
python init_extended_database.py
```

**预期输出：**
```
╔════════════════════════════════════════╗
║   扩展食物数据库初始化脚本 (105种食物)   ║
╚════════════════════════════════════════╝

============================================================
创建数据库表
============================================================

✓ 数据库表创建成功

============================================================
清除现有数据
============================================================

============================================================
开始导入食物数据
============================================================

✓ 鸡胸肉 (meat) - 3个份量选项
✓ 牛肉 (meat) - 3个份量选项
...

============================================================
数据统计
============================================================
食物种类: 105 / 105
份量选项: 280 条

✓ 数据库初始化成功完成！
```

### 如果初始化失败

**错误：`no such table: visual_portions`**
- **原因**：数据库表未创建
- **解决**：先运行 `python create_tables.py`

**错误：权限错误**
- 检查是否有写入权限
- 以管理员身份运行命令提示符

**错误：模块未找到**
- 确保在 `backend` 目录下运行脚本
- 检查Python依赖是否安装

---

## 5. 启动服务

### 方式1：使用快速启动脚本

**Windows:**
```bash
双击运行 start_simple.bat
```

**macOS/Linux:**
```bash
chmod +x start_simple.sh
./start_simple.sh
```

### 方式2：手动启动

#### 启动后端

打开第一个命令提示符窗口：

```bash
cd 智能食物记录\backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

保持此窗口打开，不要关闭。

#### 启动前端

打开第二个命令提示符窗口：

```bash
cd 智能食物记录\frontend
npm run dev -- --host 0.0.0.0
```

### 访问应用

在浏览器中打开：

```
http://localhost:5173
```

---

## 6. 常见问题解决

### 问题1：UnicodeDecodeError

**症状：**
```
UnicodeDecodeError: 'gbk' codec can't decode byte 0xff in position 0
```

**原因：**
Windows默认使用GBK编码，requirements.txt包含UTF-8字符。

**解决方案：**

1. **切换到UTF-8代码页**
   ```bash
   chcp 65001
   pip install -r requirements.txt
   ```

2. **或使用ASCII版本的requirements.txt**
   - requirements.txt已更新为纯ASCII格式

3. **或逐个安装包**
   ```bash
   pip install fastapi uvicorn sqlalchemy pydantic python-dotenv httpx
   ```

### 问题2：端口被占用

**症状：**
```
OSError: [Errno 48] Address already in use
```

**解决方案：**

**Windows:**
```bash
# 查找占用端口的进程
netstat -ano | findstr :8000
# 结束进程
taskkill /PID [进程ID] /F
```

**macOS/Linux:**
```bash
lsof -i :8000
kill -9 [进程ID]
```

### 问题3：ModuleNotFoundError

**症状：**
```
ModuleNotFoundError: No module named 'fastapi'
```

**解决方案：**

```bash
cd backend
pip install fastapi uvicorn sqlalchemy pydantic python-dotenv httpx
```

### 问题4：npm install失败

**症状：**
```
npm ERR! network timeout
```

**解决方案：**

1. **使用国内镜像**
   ```bash
   npm config set registry https://registry.npmmirror.com
   npm install
   ```

2. **或清除缓存后重试**
   ```bash
   npm cache clean --force
   npm install
   ```

### 问题5：前端无法连接后端

**症状：**
- 网络请求返回404/500错误

**解决方案：**

1. 检查后端服务是否运行
   ```
   访问 http://localhost:8000/docs
   ```

2. 检查API地址配置
   - 文件：`frontend/src/api/index.ts`
   - 确认 `API_BASE_URL` 正确

3. 检查浏览器控制台错误信息
   - 按F12打开开发者工具
   - 查看Console标签

### 问题6：手机无法访问

**症状：**
- 手机浏览器显示"无法访问"

**解决方案：**

1. **检查防火墙设置**
   - Windows安全中心 → 防火墙
   - 允许Python通过防火墙

2. **确保使用0.0.0.0启动**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   npm run dev -- --host 0.0.0.0
   ```

3. **确认在同一WiFi**
   - 电脑和手机连接相同网络

---

## 验证安装

### 运行环境检查脚本

```bash
python check_environment.py
```

应该看到所有检查项显示为绿色的 ✓。

---

## 下一步

安装完成后：

1. **启动服务**
   - Windows: 双击 `start_simple.bat`
   - 或手动启动前后端服务

2. **访问应用**
   - 电脑: http://localhost:5173
   - 手机: http://[你的IP]:5173

3. **测试功能**
   - 拍照记录食物
   - 查看今日余额
   - 设置目标

---

*文档版本: v1.0*
*更新日期: 2026-01-16*
