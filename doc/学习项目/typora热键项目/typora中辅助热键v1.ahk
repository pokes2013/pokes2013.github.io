; 打开Typora

^q::
	run C:\Program Files\Typora\Typora.exe
Return




; 分号以及分号后的内容代表注释，以下为代码解释
#IfWinActive ahk_exe Typora.exe
{
    ; alt+1 红色
    !1::addFontColor("red")
    ; alt+2 黄绿色
    !2::addFontBackground("#7FFF00")
}

; 快捷增加字体颜色
; <font color='red'>实现语法</font>

addFontColor(color){
    clipboard := "" 					; 清空剪切板
    Send {ctrl down}c{ctrl up} 			; 复制
    ; SendInput {Text} 					; 解决中文输入法问题
    SendInput {TEXT}<font color='%color%'>
    SendInput {ctrl down}v{ctrl up}		; 粘贴
    If(clipboard = ""){
        SendInput {TEXT}</font> 		; Typora 在这不会自动补充
    }else{
        SendInput {TEXT}</ 				; Typora中自动补全标签
    }
}


; 快捷高亮显示文字
; <span style="background-color: #7FFF00;">特定的文字</span>

addFontBackground(color){
    clipboard := "" 					; 清空剪切板
    Send {ctrl down}c{ctrl up} 			; 复制
    ; SendInput {Text} 					; 解决中文输入法问题
    SendInput {TEXT}<span style="background-color:%color%;">
    SendInput {ctrl down}v{ctrl up}		; 粘贴
    If(clipboard = ""){
        SendInput {TEXT}</span> 		; Typora 在这不会自动补充
    }else{
        SendInput {TEXT}</ 				; Typora中自动补全标签
    }
}