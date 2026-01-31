; 打开 Typora（Ctrl+Q）- 避免重复启动，直接激活已有窗口
^q::
	If !WinExist("ahk_exe Typora.exe")
		run C:\Program Files\Typora\Typora.exe
	Else
		WinActivate ahk_exe Typora.exe
Return

; 仅在 Typora 激活时生效的快捷键
#IfWinActive ahk_exe Typora.exe
    ; Alt+1 设置文字为【红色+加粗】
    !1::addBoldFontColor("red")
    ; Alt+2 设置文字为【橘色+加粗】（新增功能）
    !2::addBoldFontColor("orange")  ; 也可使用 #ff7b00 替代 orange
    ; Alt+3 设置文字背景为粉色
    !3::addFontBackground("#f7df06")
    ; Alt+4 设置文字背景为粉色
    !4::addFontBackground("#aff804f1")
    ; Alt+9 设置文字背景为黄绿色
    !9::addFontBackground("#7FFF00")
#IfWinActive  ; 结束窗口上下文判断

; 加粗+字体颜色函数（已修复，无需修改）
addBoldFontColor(color){
    ; 1. 先暂停一小段时间，确保Typora响应选中状态
    Sleep, 100
    
    ; 2. 清空剪切板并强制复制选中文字（重复复制确保成功）
    clipboard := ""
    Send ^c  ; 第一次复制
    Sleep, 200  ; 延长等待，适配Typora响应速度
    Send ^c  ; 第二次复制，确保剪切板拿到内容
    ClipWait, 1  ; 最长等待1秒，直到剪切板有内容
    if ErrorLevel {  ; 仍复制失败（无选中内容）
        selectedText := ""
    } else {
        selectedText := clipboard  ; 保存复制的文字，避免后续操作覆盖
    }
    
    ; 3. 删除原选中的文字（避免重复），再输入完整的样式+文字
    Send {Delete}  ; 删除选中的文字
    Sleep, 50
    
    ; 4. 拼接完整的加粗+颜色语法并输入
    if (selectedText = "") {
        ; 无选中文字：生成空标签，光标定位在中间
        SendInput {TEXT}**<span style="color:%color%;">|</span>**
        Send {Left}  ; 光标移到 | 的位置（可直接输入文字）
    } else {
        ; 有选中文字：完整包裹样式
        SendInput {TEXT}**<span style="color:%color%;">%selectedText%</span>**
    }
    
    clipboard := ""  ; 清空剪切板
}

; 背景高亮函数（已修复，无需修改）
addFontBackground(color){
    ; 1. 暂停+重复复制，确保拿到选中文字
    Sleep, 100
    clipboard := ""
    Send ^c
    Sleep, 200
    Send ^c
    ClipWait, 1
    if ErrorLevel {
        selectedText := ""
    } else {
        selectedText := clipboard
    }
    
    ; 2. 删除原文字，输入完整高亮语法
    Send {Delete}
    Sleep, 50
    
    if (selectedText = "") {
        ; 无选中文字：生成空标签，光标定位中间
        SendInput {TEXT}<span style="background-color:%color%;">|</span>
        Send {Left}
    } else {
        ; 有选中文字：完整包裹
        SendInput {TEXT}<span style="background-color:%color%;">%selectedText%</span>
    }
    
    clipboard := ""
}