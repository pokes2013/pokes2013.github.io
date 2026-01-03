:softshare
IF "%~1"=="" GOTO :EOF
ffmpeg -i "%~1" -vf scale=1280:-2 "%~dpn1_ok.jpg"
SHIFT & GOTO:softshare