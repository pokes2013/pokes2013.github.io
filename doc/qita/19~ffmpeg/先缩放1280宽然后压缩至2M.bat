@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
:: 2MB 大小阈值
set "MAX_SIZE=2097152"
set "OUT_DIR=outfiles"

:: 不存在则创建输出文件夹
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"

:: 遍历当前目录图片格式
for %%i in (*.jpg *.jpeg *.png) do (
    set "input=%%i"
    set "output=%OUT_DIR%\%%~ni_ok.jpg"
    echo 正在处理：!input!
    :: 首次缩放压缩
    ffmpeg -i "!input!" -vf scale=1280:-2 -q:v 8 "!output!"
    
    for %%f in ("!output!") do set "fsize=%%~zf"
    set "q=8"
    
    :: 循环降质压到2M以内
    :size_loop
    if !fsize! leq !MAX_SIZE! goto end_loop
    set /a q+=2
    ffmpeg -i "!output!" -q:v !q! "!output!"
    for %%f in ("!output!") do set "fsize=%%~zf"
    goto size_loop
    :end_loop
    echo 已保存至：!output!
    echo.
)
echo ======================
echo 全部图片压缩完成，文件输出至 outfiles 文件夹
pause