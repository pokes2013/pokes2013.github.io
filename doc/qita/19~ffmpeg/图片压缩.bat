@echo off
chcp 65001 >nul
:softshare
IF "%~1"=="" GOTO :EOF
set "source=%~1"
set "outfile=%~dpn1_ok.jpg"
:: 第一步：固定宽度1280缩放导出
ffmpeg -i "%source%" -vf scale=1280:-2 -q:v 8 "%outfile%"
:: 判断文件是否大于2MB（2*1024*1024=2097152字节）
for %%f in ("%outfile%") do set filesize=%%~zf
if %filesize% gtr 2097152 (
    echo 文件超过2MB，二次压缩降质处理
    ffmpeg -i "%outfile%" -q:v 15 "%outfile%"
)
SHIFT & GOTO:softshare