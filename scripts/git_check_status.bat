@echo off
REM =============================================
REM Git状态检查脚本 - 智能食物记录项目
REM 功能: 快速查看当前Git更改状态
REM =============================================

setlocal enabledelayedexpansion
set "PROJECT_DIR=%~dp0"
set "TITLE=Git状态检查 - 智能食物记录"

REM 设置颜色代码
set "GREEN=[92m"
set "RED=[91m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "WHITE=[97m"
set "GRAY=[90m"
set "RESET=[0m"

title %TITLE%

REM 进入项目目录
cd /d "%PROJECT_DIR%"

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%   Git状态检查 - 智能食物记录项目   %RESET%
echo %CYAN%========================================%RESET%
echo.

REM ============================================
REM 1. 基本状态信息
REM ============================================
echo %YELLOW%[基本信息]%RESET%
echo.

REM 当前分支
for /f "tokens=*" %%a in ('git branch --show-current') do set "CURRENT_BRANCH=%%a"
echo %WHITE%当前分支:%RESET% %GREEN%!CURRENT_BRANCH!%RESET%

REM 远程仓库
for /f "tokens=*" %%a in ('git remote get-url origin') do set "REMOTE_URL=%%a"
echo %WHITE%远程仓库:%RESET% !REMOTE_URL!

REM 最新提交
echo.
echo %WHITE%最新提交:%RESET%
git log -1 --oneline --decorate
echo.

REM ============================================
REM 2. 工作区状态
REM ============================================
echo %WHITE%----------------------------------------%RESET%
echo.
echo %YELLOW%[工作区状态]%RESET%
echo.

REM 检查是否有更改
git diff-index --quiet HEAD --
if %errorlevel% equ 0 (
    echo %GREEN%✓ 工作区干净，没有更改%RESET%
) else (
    echo %YELLOW%⚠ 检测到未提交的更改%RESET%
    echo.

    REM 显示已修改文件
    echo %BLUE%已修改的文件:%RESET%
    git diff --name-only HEAD
    echo.

    REM 显示更改统计
    echo %BLUE%更改统计:%RESET%
    git diff --stat HEAD
)

echo.

REM ============================================
REM 3. 暂存区状态
REM ============================================
echo %YELLOW%[暂存区状态]%RESET%
echo.

git diff --cached --quiet
if %errorlevel% equ 0 (
    echo %GREEN%✓ 暂存区为空%RESET%
) else (
    echo %YELLOW%⚠ 暂存区有文件待提交%RESET%
    echo.
    echo %BLUE%已暂存的文件:%RESET%
    git diff --cached --name-only
)

echo.

REM ============================================
REM 4. 未跟踪文件
REM ============================================
echo %YELLOW%[未跟踪文件]%RESET%
echo.

set "UNTRACKED_COUNT=0"
for /f %%a in ('git ls-files --others --exclude-standard ^| find /c /v ""') do set "UNTRACKED_COUNT=%%a"

if !UNTRACKED_COUNT! equ 0 (
    echo %GREEN%✓ 没有未跟踪的文件%RESET%
) else (
    echo %YELLOW%⚠ 发现 !UNTRACKED_COUNT! 个未跟踪文件%RESET%
    echo.
    echo %BLUE%未跟踪文件列表:%RESET%
    git ls-files --others --exclude-standard
)

echo.

REM ============================================
REM 5. 远程同步状态
REM ============================================
echo %YELLOW%[远程同步状态]%RESET%
echo.

git fetch origin --quiet 2>nul

REM 检查本地是否落后
for /f %%a in ('git rev-list --count HEAD..@{u} 2^>nul') do set "BEHIND_COUNT=%%a"
if "!BEHIND_COUNT!"=="" set "BEHIND_COUNT=0"

REM 检查本地是否领先
for /f %%a in ('git rev-list --count @{u}..HEAD 2^>nul') do set "AHEAD_COUNT=%%a"
if "!AHEAD_COUNT!"=="" set "AHEAD_COUNT=0"

if !BEHIND_COUNT! equ 0 (
    if !AHEAD_COUNT! equ 0 (
        echo %GREEN%✓ 与远程同步%RESET%
    ) else (
        echo %YELLOW%⚠ 本地领先远程 !AHEAD_COUNT! 个提交%RESET%
        echo %GRAY%  建议: git push origin main%RESET%
    )
) else (
    echo %YELLOW%⚠ 本地落后远程 !BEHIND_COUNT! 个提交%RESET%
    echo %GRAY%  建议: git pull origin main%RESET%
)

if !AHEAD_COUNT! gtr 0 (
    if !BEHIND_COUNT! gtr 0 (
        echo %RED%✗ 本地与远程有分歧%RESET%
        echo %GRAY%  建议: git pull origin main --rebase%RESET%
    )
)

echo.

REM ============================================
REM 6. 下一步操作建议
REM ============================================
echo %WHITE%----------------------------------------%RESET%
echo.
echo %YELLOW%[下一步操作建议]%RESET%
echo.

git diff-index --quiet HEAD --
if %errorlevel% neq 0 (
    echo %CYAN%有未提交的更改，建议:%RESET%
    echo   1. 运行 git_update.bat 提交更改
    echo   2. 或手动执行: git add . ^&^& git commit -m "类型: 描述"
    echo.
)

if !BEHIND_COUNT! gtr 0 (
    echo %CYAN%远程有新更新，建议:%RESET%
    echo   1. 执行: git pull origin main
    echo.
)

if !AHEAD_COUNT! gtr 0 (
    if !BEHIND_COUNT! equ 0 (
        echo %CYAN%本地有未推送的提交，建议:%RESET%
        echo   1. 执行: git push origin main
        echo.
    )
)

if !UNTRACKED_COUNT! gtr 0 (
    echo %CYAN%有未跟踪文件，建议:%RESET%
    echo   1. 添加到.gitignore（如果不需要提交）
    echo   2. 或使用 git add . 添加到版本控制
    echo.
)

REM 如果一切正常
git diff-index --quiet HEAD --
if %errorlevel% equ 0 (
    if !BEHIND_COUNT! equ 0 (
        if !AHEAD_COUNT! equ 0 (
            if !UNTRACKED_COUNT! equ 0 (
                echo %GREEN%✓ 一切正常，无需操作%RESET%
                echo.
            )
        )
    )
)

echo %WHITE%----------------------------------------%RESET%
echo.

REM ============================================
REM 7. 快捷操作提示
REM ============================================
echo %GRAY%快捷命令:%RESET%
echo   git_update.bat      - 一键提交并推送
echo   git_undo_last.bat   - 撤销最后一次提交
echo.

pause
