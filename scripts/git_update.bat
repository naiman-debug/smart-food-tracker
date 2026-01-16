@echo off
REM =============================================
REM Git一键更新脚本 - 智能食物记录项目
REM 功能: 自动执行git add, commit, push操作
REM =============================================

setlocal enabledelayedexpansion
set "PROJECT_DIR=%~dp0"
set "TITLE=Git更新助手 - 智能食物记录"

REM 设置颜色代码
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "WHITE=[97m"
set "RESET=[0m"

title %TITLE%

REM 进入项目目录
cd /d "%PROJECT_DIR%"

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%   Git更新助手 - 智能食物记录项目   %RESET%
echo %CYAN%========================================%RESET%
echo.

REM ============================================
REM 步骤1: 检查Git状态
REM ============================================
echo %YELLOW%[步骤1/4]%RESET% 检查当前Git状态...
echo.

git status

echo.
echo %WHITE%----------------------------------------%RESET%
echo.

REM ============================================
REM 步骤2: 显示将要提交的文件
REM ============================================
echo %YELLOW%[步骤2/4]%RESET% 分析更改内容...
echo.

REM 检查是否有更改
git diff-index --quiet HEAD --
if %errorlevel% equ 0 (
    echo %GREEN%✓ 没有检测到更改，无需提交%RESET%
    echo.
    pause
    exit /b 0
)

REM 显示修改的文件
echo %BLUE%已修改的文件:%RESET%
git diff --name-only HEAD

echo.

REM 显示未跟踪的文件
echo %BLUE%未跟踪的新文件:%RESET%
git ls-files --others --exclude-standard

echo.
echo %WHITE%----------------------------------------%RESET%
echo.

REM ============================================
REM 步骤3: 输入提交消息
REM ============================================
echo %YELLOW%[步骤3/4]%RESET% 输入提交消息
echo.
echo %WHITE%提交消息格式：类型: 简短描述%RESET%
echo.
echo %CYAN%可选类型:%RESET%
echo   feat  - 新功能
echo   fix   - Bug修复
echo   docs  - 文档更新
echo   test  - 测试相关
echo   chore - 维护任务
echo.
echo %CYAN%示例:%RESET%
echo   feat: 添加用户头像上传功能
echo   fix: 修复登录页面响应问题
echo   docs: 更新API文档
echo.

set /p COMMIT_MSG="请输入提交消息: "

REM 验证输入不为空
if "!COMMIT_MSG!"=="" (
    echo.
    echo %RED%✗ 提交消息不能为空！%RESET%
    echo.
    pause
    exit /b 1
)

REM 自动添加类型前缀（如果没有）
echo !COMMIT_MSG! | findstr /i /b "feat: fix: docs: test: chore: refactor: style: perf:" >nul
if !errorlevel! neq 0 (
    echo.
    echo %YELLOW%注意: 未检测到类型前缀，已自动添加 'chore:'%RESET%
    set "COMMIT_MSG=chore: !COMMIT_MSG!"
)

echo.
echo %WHITE%----------------------------------------%RESET%
echo.

REM ============================================
REM 步骤4: 执行Git操作
REM ============================================
echo %YELLOW%[步骤4/4]%RESET% 执行Git操作...
echo.

REM 添加所有更改
echo %BLUE%→ 添加文件到暂存区...%RESET%
git add .
if %errorlevel% neq 0 (
    echo %RED%✗ git add 失败！%RESET%
    pause
    exit /b 1
)

REM 创建提交
echo %BLUE%→ 创建提交...%RESET%
git commit -m "!COMMIT_MSG!"
if %errorlevel% neq 0 (
    echo %RED%✗ git commit 失败！%RESET%
    pause
    exit /b 1
)

REM 推送到远程
echo %BLUE%→ 推送到GitHub...%RESET%
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo %RED%✗ git push 失败！%RESET%
    echo.
    echo %YELLOW%可能原因:%RESET%
    echo   1. 网络连接问题
    echo   2. 远程有新的提交（需要先pull）
    echo   3. 认证信息过期
    echo.
    echo %CYAN%建议执行:%RESET% git pull origin main
    echo.
    pause
    exit /b 1
)

echo.
echo %GREEN%========================================%RESET%
echo %GREEN%       ✓ 更新成功完成！%RESET%
echo %GREEN%========================================%RESET%
echo.
echo %WHITE%提交消息:%RESET% !COMMIT_MSG!
echo %WHITE%提交时间:%RESET% %date% %time%
echo.

REM 显示最新提交
echo %CYAN%最新提交:%RESET%
git log -1 --oneline
echo.

pause
