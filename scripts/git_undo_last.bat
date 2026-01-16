@echo off
REM =============================================
REM Git回滚助手脚本 - 智能食物记录项目
REM 功能: 安全地撤销最后一次提交
REM =============================================

setlocal enabledelayedexpansion
set "PROJECT_DIR=%~dp0"
set "TITLE=Git回滚助手 - 智能食物记录"

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
echo %CYAN%   Git回滚助手 - 智能食物记录项目   %RESET%
echo %CYAN%========================================%RESET%
echo.

REM ============================================
REM 步骤1: 显示当前状态
REM ============================================
echo %YELLOW%[当前状态]%RESET%
echo.

REM 显示最新提交
echo %WHITE%最新提交:%RESET%
git log -1 --oneline --decorate
echo.

REM 显示提交详情
echo %WHITE%提交详情:%RESET%
git log -1 --pretty=format:"%%h - %%an, %%ar : %%s" --decorate
echo.

REM 显示更改的文件
echo %WHITE%此次提交修改的文件:%RESET%
git log -1 --name-only --pretty=format:""
echo.

REM 检查是否已推送
for /f %%a in ('git rev-list --count @{u}..HEAD 2^>nul') do set "AHEAD_COUNT=%%a"
if "!AHEAD_COUNT!"=="" set "AHEAD_COUNT=0"

if !AHEAD_COUNT! gtr 0 (
    echo %GREEN%✓ 此提交仅存在于本地，尚未推送到远程%RESET%
) else (
    echo %RED%⚠ 警告: 此提交已推送到远程！%RESET%
    echo %YELLOW%  撤销操作可能影响其他协作者%RESET%
)

echo.
echo %WHITE%----------------------------------------%RESET%
echo.

REM ============================================
REM 步骤2: 选择撤销方式
REM ============================================
echo %YELLOW%[撤销方式选择]%RESET%
echo.
echo %CYAN%请选择撤销方式:%RESET%
echo.
echo %WHITE%1.%RESET% %GREEN%Soft撤销%RESET% - 撤销提交，保留文件在暂存区
echo   %GRAY%适用: 修改提交消息或添加遗漏的文件%RESET%
echo.
echo %WHITE%2.%RESET% %YELLOW%Mixed撤销%RESET% - 撤销提交和暂存，保留文件在工作区
echo   %GRAY%适用: 重新编辑文件后再次提交%RESET%
echo.
echo %WHITE%3.%RESET% %RED%Hard撤销%RESET% - 完全删除提交和所有更改
echo   %GRAY%适用: 确认提交完全错误%RESET%
echo.
echo %WHITE%4.%RESET% %BLUE%Revert撤销%RESET% - 创建新提交来撤销（推荐用于已推送）
echo   %GRAY%适用: 已推送到远程的安全撤销方式%RESET%
echo.
echo %WHITE%0.%RESET% 取消操作
echo.

set /p CHOICE="请输入选择 (0-4): "

REM 验证输入
if "!CHOICE!"=="0" (
    echo.
    echo %YELLOW%操作已取消%RESET%
    echo.
    pause
    exit /b 0
)

if "!CHOICE!"=="1" goto :UNDO_SOFT
if "!CHOICE!"=="2" goto :UNDO_MIXED
if "!CHOICE!"=="3" goto :UNDO_HARD
if "!CHOICE!"=="4" goto :UNDO_REVERT

echo.
echo %RED%✗ 无效的选择！%RESET%
echo.
pause
exit /b 1

REM ============================================
REM Soft撤销
REM ============================================
:UNDO_SOFT
echo.
echo %YELLOW%[执行Soft撤销]%RESET%
echo.
echo %BLUE%→ 撤销提交，保留更改在暂存区...%RESET%
echo.
git reset --soft HEAD~1

if %errorlevel% equ 0 (
    call :SUCCESS "文件已保留在暂存区，可继续编辑"
) else (
    call :FAILED "git reset --soft 失败"
)
exit /b %errorlevel%

REM ============================================
REM Mixed撤销
REM ============================================
:UNDO_MIXED
echo.
echo %YELLOW%[执行Mixed撤销]%RESET%
echo.
echo %BLUE%→ 撤销提交和暂存，保留更改在工作区...%RESET%
echo.
git reset --mixed HEAD~1

if %errorlevel% equ 0 (
    call :SUCCESS "文件已保留在工作区，可使用 git add 重新添加"
) else (
    call :FAILED "git reset --mixed 失败"
)
exit /b %errorlevel%

REM ============================================
REM Hard撤销
REM ============================================
:UNDO_HARD
REM 二次确认
echo.
echo %RED%⚠ 警告: Hard撤销将永久删除所有更改！%RESET%
echo.
set /p CONFIRM="确认执行Hard撤销? (输入 YES 继续): "
if not "!CONFIRM!"=="YES" (
    echo.
    echo %YELLOW%操作已取消%RESET%
    echo.
    pause
    exit /b 0
)

echo.
echo %YELLOW%[执行Hard撤销]%RESET%
echo.
echo %BLUE%→ 完全删除提交和所有更改...%RESET%
echo.
git reset --hard HEAD~1

if %errorlevel% equ 0 (
    call :SUCCESS "提交和所有更改已被永久删除"
) else (
    call :FAILED "git reset --hard 失败"
)
exit /b %errorlevel%

REM ============================================
REM Revert撤销
REM ============================================
:UNDO_REVERT
echo.
echo %YELLOW%[执行Revert撤销]%RESET%
echo.
echo %BLUE%→ 创建新提交来撤销上次更改...%RESET%
echo.
git revert HEAD --no-edit

if %errorlevel% equ 0 (
    echo.
    echo %GREEN%✓ Revert提交已创建%RESET%
    echo.
    echo %CYAN%如需推送到远程:%RESET%
    echo   git push origin main
    echo.
) else (
    call :FAILED "git revert 失败（可能有冲突需要解决）"
)
exit /b %errorlevel%

REM ============================================
REM 成功处理子程序
REM ============================================
:SUCCESS
echo.
echo %GREEN%========================================%RESET%
echo %GREEN%           ✓ 撤销成功完成%RESET%
echo %GREEN%========================================%RESET%
echo.
echo %WHITE%~1%RESET%
echo.
echo %CYAN%当前状态:%RESET%
git status
echo.
echo %CYAN%最新提交:%RESET%
git log -1 --oneline
echo.
pause
exit /b 0

REM ============================================
REM 失败处理子程序
REM ============================================
:FAILED
echo.
echo %RED%========================================%RESET%
echo %RED%           ✗ 撤销操作失败%RESET%
echo %RED%========================================%RESET%
echo.
echo %WHITE%~1%RESET%
echo.
echo %YELLOW%可能原因:%RESET%
echo   1. 只有初始提交，无法撤销
echo   2. Git仓库状态异常
echo   3. 文件系统权限问题
echo.
echo %CYAN%建议:%RESET%
echo   查看Git状态: git status
echo   查看提交历史: git log --oneline
echo.
pause
exit /b 1
