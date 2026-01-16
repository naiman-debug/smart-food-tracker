# APK打包指南

> 使用Capacitor将Vue应用转为Android APK

---

## 目录

1. [环境准备](#1-环境准备)
2. [Capacitor集成](#2-capacitor集成)
3. [API地址配置](#3-api地址配置)
4. [构建APK](#4-构建apk)
5. [常见问题](#5-常见问题)

---

## 1. 环境准备

### 必需软件

| 软件 | 版本要求 | 下载地址 |
|------|----------|----------|
| JDK | 11+ | https://adoptium.net/ |
| Android Studio | 最新版 | https://developer.android.com/studio |
| Node.js | 16+ | https://nodejs.org/ |

### 环境变量配置

**Windows:**
```bash
# 设置 JAVA_HOME
setx JAVA_HOME "C:\Program Files\Java\jdk-11"
# 添加到 PATH
setx PATH "%JAVA_HOME%\bin;%PATH%"
```

**macOS/Linux:**
```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk
export PATH=$JAVA_HOME/bin:$PATH
```

### 验证安装

```bash
java -version
javac -version
npm --version
```

---

## 2. Capacitor集成

### 步骤1：安装Capacitor

在项目根目录执行：

```bash
cd frontend
npm install @capacitor/core @capacitor/cli
npx cap init
```

配置信息：
```
App name: 智能食物记录
App ID: com.smartfood.app
Web dir: dist
```

### 步骤2：安装Android平台

```bash
npm install @capacitor/android
npx cap add android
```

### 步骤3：配置Android

编辑 `android/app/src/main/AndroidManifest.xml`，添加网络权限：

```xml
<manifest>
    <!-- 添加网络权限 -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <application ...>
        ...
    </application>
</manifest>
```

### 步骤4：配置capacitor.config.ts

编辑 `frontend/capacitor.config.ts`：

```typescript
import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'com.smartfood.app',
  appName: '智能食物记录',
  webDir: 'dist',
  bundledWebRuntime: false,
  server: {
    // 开发模式：连接本地后端
    androidScheme: 'http',
    // 或者使用代理
    proxyUrl: 'http://YOUR_COMPUTER_IP:8000'
  }
};

export default config;
```

---

## 3. API地址配置

### 方案1：本地开发（连接电脑后端）

**修改 `frontend/src/api/index.ts`：**

```typescript
// 获取本机IP
const API_BASE_URL = 'http://192.168.1.100:8000/api'; // 替换为你的IP
```

**或在Capacitor配置中使用代理：**

```typescript
// capacitor.config.ts
server: {
  androidScheme: 'http',
  proxyUrl: 'http://192.168.1.100:8000',
  cleartext: true
}
```

### 方案2：云服务部署

**部署后端到云服务器后，修改API地址：**

```typescript
// frontend/src/api/index.ts
const API_BASE_URL = 'https://your-backend-domain.com/api';
```

### 方案3：使用环境变量

**创建 `.env.production` 文件：**

```bash
VITE_API_BASE_URL=https://your-backend-domain.com/api
```

**在 `api/index.ts` 中使用：**

```typescript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
```

---

## 4. 构建APK

### 步骤1：构建前端

```bash
cd frontend
npm run build
```

### 步骤2：同步资源到Android

```bash
npx cap sync android
```

### 步骤3：打开Android Studio

```bash
npx cap open android
```

### 步骤4：在Android Studio中构建

1. 等待Gradle同步完成
2. 选择 **Build → Build Bundle(s) / APK(s) → Build APK(s)**
3. 等待构建完成
4. APK位置：`android/app/build/outputs/apk/debug/app-debug.apk`

### 步骤5：安装到手机

**通过USB安装：**
```bash
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

**或直接传输APK文件到手机安装**

---

## 5. 常见问题

### 问题1：Gradle同步失败

**解决方案：**

1. 检查网络连接（需要访问Google Maven）
2. 使用国内镜像源，编辑 `android/build.gradle`：

```gradle
repositories {
    maven { url 'https://maven.aliyun.com/repository/public/' }
    maven { url 'https://maven.aliyun.com/repository/google/' }
    google()
    mavenCentral()
}
```

### 问题2：应用无法连接后端

**检查清单：**

- [ ] AndroidManifest.xml 是否添加了网络权限
- [ ] API地址是否正确（http vs https）
- [ ] 手机和服务器是否在同一网络
- [ ] 防火墙是否允许连接

### 问题3：打包时签名错误

**解决方案：**

生成调试签名（debug signing已自动配置）

如需发布签名，创建 `keystore.properties`：

```properties
storePassword=your_password
keyPassword=your_password
keyAlias=your_key_alias
storeFile=path/to/keystore.jks
```

### 问题4：应用安装失败

**可能原因：**

1. 手机开启了"未知来源"限制
   - 设置 → 安全 → 允许安装未知来源应用

2. APK签名问题
   - 使用正确的签名配置

3. Android版本不兼容
   - 检查 `minSdkVersion` 配置

---

## 调试APK

### 查看日志

```bash
adb logcat | grep "smartfood"
```

### 查看网络请求

在Chrome中：
1. 手机启用USB调试
2. Chrome打开 `chrome://inspect`
3. 选择设备进行调试

---

## 发布准备

### 修改应用信息

**编辑 `android/app/src/main/AndroidManifest.xml`：**

```xml
<manifest>
    <application
        android:label="智能食物记录"
        android:icon="@mipmap/ic_launcher">
        ...
    </application>
</manifest>
```

### 生成发布版APK

1. 配置签名
2. 选择 **Build → Generate Signed Bundle / APK**
3. 选择 "APK"
4. 完成签名配置
5. 构建完成后APK位于 `app/release/`

---

## 快速命令参考

```bash
# 初始化Capacitor
npm install @capacitor/core @capacitor/cli
npx cap init

# 添加Android平台
npm install @capacitor/android
npx cap add android

# 构建并同步
npm run build
npx cap sync android

# 打开Android Studio
npx cap open android

# 命令行构建APK
cd android
./gradlew assembleDebug

# 安装到设备
cd ..
npx cap run android
```

---

*文档版本: v1.0*
*更新日期: 2026-01-16*
